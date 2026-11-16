import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { deflateSync } from 'node:zlib';
import { join } from 'node:path';

const source = readFileSync(join(import.meta.dirname, 'assets', 'rift.ppm'));
const marker = Buffer.from('\n');
const headerEnd = source.indexOf(marker, source.indexOf(marker, source.indexOf(marker) + 1) + 1) + 1;
const header = source.subarray(0, headerEnd).toString('ascii').trim().split(/\s+/);
if (header[0] !== 'P6' || Number(header[3]) !== 255) throw new Error('Expected 8-bit binary PPM');
const width = Number(header[1]);
const height = Number(header[2]);
const pixels = source.subarray(headerEnd);
if (width > 1024 || height > 1024 || pixels.length !== width * height * 3) throw new Error('Invalid artwork dimensions');

const crcTable = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  crcTable[n] = c >>> 0;
}
function chunk(type: string, data: Buffer): Buffer {
  const name = Buffer.from(type, 'ascii');
  const body = Buffer.concat([name, data]);
  let crc = 0xffffffff;
  for (const byte of body) crc = crcTable[(crc ^ byte) & 255] ^ (crc >>> 8);
  const length = Buffer.alloc(4); length.writeUInt32BE(data.length);
  const checksum = Buffer.alloc(4); checksum.writeUInt32BE((crc ^ 0xffffffff) >>> 0);
  return Buffer.concat([length, body, checksum]);
}
const scanlines = Buffer.alloc(height * (width * 3 + 1));
for (let y = 0; y < height; y++) pixels.copy(scanlines, y * (width * 3 + 1) + 1, y * width * 3, (y + 1) * width * 3);
const dimensions = Buffer.alloc(13);
dimensions.writeUInt32BE(width, 0); dimensions.writeUInt32BE(height, 4);
dimensions[8] = 8; dimensions[9] = 2;
const png = Buffer.concat([
  Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
  chunk('IHDR', dimensions), chunk('IDAT', deflateSync(scanlines, { level: 9 })), chunk('IEND', Buffer.alloc(0)),
]);
const out = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(out, { recursive: true });
writeFileSync(join(out, 'entry.png'), png);
