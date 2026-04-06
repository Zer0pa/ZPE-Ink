using System;
using System.Collections.Generic;
using System.Text;

namespace ZPE.Ink {
    public sealed class ZpeInkException : Exception {
        public ZpeInkException(string message) : base(message) {}
    }

    public sealed class ZpeInkHeader {
        public byte Version { get; private set; }
        public byte Mode { get; private set; }
        public byte Flags { get; private set; }
        public ushort StrokeCount { get; private set; }
        public uint Seed { get; private set; }
        public uint PayloadLength { get; private set; }
        public uint PayloadCrc { get; private set; }

        public ZpeInkHeader(byte version, byte mode, byte flags, ushort strokeCount, uint seed, uint payloadLength, uint payloadCrc) {
            Version = version;
            Mode = mode;
            Flags = flags;
            StrokeCount = strokeCount;
            Seed = seed;
            PayloadLength = payloadLength;
            PayloadCrc = payloadCrc;
        }
    }

    public sealed class ZpeInkPoint {
        public int X { get; private set; }
        public int Y { get; private set; }
        public int Pressure { get; private set; }
        public int Tilt { get; private set; }
        public int Azimuth { get; private set; }

        public ZpeInkPoint(int x, int y, int pressure, int tilt, int azimuth) {
            X = x;
            Y = y;
            Pressure = pressure;
            Tilt = tilt;
            Azimuth = azimuth;
        }
    }

    public sealed class ZpeInkStroke {
        public IReadOnlyList<int> X { get; private set; }
        public IReadOnlyList<int> Y { get; private set; }
        public IReadOnlyList<int> Pressure { get; private set; }
        public IReadOnlyList<int> Tilt { get; private set; }
        public IReadOnlyList<int> Azimuth { get; private set; }

        public ZpeInkStroke(List<int> x, List<int> y, List<int> pressure, List<int> tilt, List<int> azimuth) {
            X = x.AsReadOnly();
            Y = y.AsReadOnly();
            Pressure = pressure.AsReadOnly();
            Tilt = tilt.AsReadOnly();
            Azimuth = azimuth.AsReadOnly();
        }

        public IReadOnlyList<ZpeInkPoint> Points {
            get {
                var points = new List<ZpeInkPoint>(X.Count);
                for (var i = 0; i < X.Count; i++) {
                    points.Add(new ZpeInkPoint(X[i], Y[i], Pressure[i], Tilt[i], Azimuth[i]));
                }
                return points.AsReadOnly();
            }
        }

        public string CanonicalJson() {
            return "{\"azimuth\":" + SerializeArray(Azimuth)
                + ",\"pressure\":" + SerializeArray(Pressure)
                + ",\"tilt\":" + SerializeArray(Tilt)
                + ",\"x\":" + SerializeArray(X)
                + ",\"y\":" + SerializeArray(Y)
                + "}";
        }

        private static string SerializeArray(IReadOnlyList<int> values) {
            var builder = new StringBuilder();
            builder.Append("[");
            for (var i = 0; i < values.Count; i++) {
                if (i > 0) {
                    builder.Append(",");
                }
                builder.Append(values[i]);
            }
            builder.Append("]");
            return builder.ToString();
        }
    }

    public sealed class ZpeInkDecoded {
        public string Magic { get; private set; }
        public byte Version { get; private set; }
        public string Mode { get; private set; }
        public byte Flags { get; private set; }
        public uint Seed { get; private set; }
        public IReadOnlyList<ZpeInkStroke> Strokes { get; private set; }

        public ZpeInkDecoded(string magic, byte version, string mode, byte flags, uint seed, List<ZpeInkStroke> strokes) {
            Magic = magic;
            Version = version;
            Mode = mode;
            Flags = flags;
            Seed = seed;
            Strokes = strokes.AsReadOnly();
        }

        public string CanonicalJson() {
            var builder = new StringBuilder();
            builder.Append("{\"flags\":");
            builder.Append(Flags);
            builder.Append(",\"magic\":\"");
            builder.Append(Magic);
            builder.Append("\",\"mode\":\"");
            builder.Append(Mode);
            builder.Append("\",\"seed\":");
            builder.Append(Seed);
            builder.Append(",\"strokes\":[");
            for (var i = 0; i < Strokes.Count; i++) {
                if (i > 0) {
                    builder.Append(",");
                }
                builder.Append(Strokes[i].CanonicalJson());
            }
            builder.Append("],\"version\":");
            builder.Append(Version);
            builder.Append("}");
            return builder.ToString();
        }
    }

    // Native SDK parity contract mirror for hosts with .NET runtime available.
    public static class ZpeInk {
        public static string Version {
            get { return "0.1.0"; }
        }

        private const int HeaderBytes = 22;
        private const byte FlagPressure = 0b001;
        private const byte FlagTilt = 0b010;
        private const byte FlagAzimuth = 0b100;

        public static ZpeInkHeader ParseHeader(byte[] bytes) {
            if (bytes == null || bytes.Length < HeaderBytes) {
                throw new ZpeInkException("stream too short for header");
            }
            if (bytes[0] != (byte)'Z' || bytes[1] != (byte)'P' || bytes[2] != (byte)'I' || bytes[3] != (byte)'N' || bytes[4] != (byte)'K') {
                throw new ZpeInkException("invalid magic");
            }

            var offset = 5;
            var version = bytes[offset++];
            var mode = bytes[offset++];
            var flags = bytes[offset++];
            var strokeCount = ReadU16(bytes, ref offset);
            var seed = ReadU32(bytes, ref offset);
            var payloadLength = ReadU32(bytes, ref offset);
            var payloadCrc = ReadU32(bytes, ref offset);

            return new ZpeInkHeader(version, mode, flags, strokeCount, seed, payloadLength, payloadCrc);
        }

        public static IReadOnlyList<int> DecodeHeader(byte[] bytes) {
            var header = ParseHeader(bytes);
            return new List<int> {
                header.Version,
                header.Mode,
                header.Flags,
                header.StrokeCount,
            }.AsReadOnly();
        }

        public static ZpeInkDecoded Decode(byte[] bytes) {
            var header = ParseHeader(bytes);
            if (header.Version != 1) {
                throw new ZpeInkException("unsupported version: " + header.Version);
            }

            var mode = ModeName(header.Mode);
            if ((header.Flags & FlagPressure) == 0) {
                throw new ZpeInkException("pressure channel is mandatory");
            }

            var payload = new byte[bytes.Length - HeaderBytes];
            Buffer.BlockCopy(bytes, HeaderBytes, payload, 0, payload.Length);
            if (payload.Length != header.PayloadLength) {
                throw new ZpeInkException("payload length mismatch");
            }
            if (Crc32(payload) != header.PayloadCrc) {
                throw new ZpeInkException("payload CRC mismatch");
            }

            var strokes = new List<ZpeInkStroke>(header.StrokeCount);
            var hasTilt = (header.Flags & FlagTilt) != 0;
            var hasAzimuth = (header.Flags & FlagAzimuth) != 0;
            var offset = 0;

            for (var strokeIndex = 0; strokeIndex < header.StrokeCount; strokeIndex++) {
                var pointCount = ReadU16(payload, ref offset);
                if (pointCount == 0) {
                    throw new ZpeInkException("stroke[" + strokeIndex + "] has zero points");
                }

                var x0 = ReadI32(payload, ref offset);
                var y0 = ReadI32(payload, ref offset);

                var xLength = checked((int) ReadU32(payload, ref offset));
                var xEnd = CheckedEnd(offset, xLength, payload.Length, "x stream");
                var xDeltas = DecodeDeltaRle(payload, offset, xEnd - offset, pointCount - 1);
                offset = xEnd;

                var yLength = checked((int) ReadU32(payload, ref offset));
                var yEnd = CheckedEnd(offset, yLength, payload.Length, "y stream");
                var yDeltas = DecodeDeltaRle(payload, offset, yEnd - offset, pointCount - 1);
                offset = yEnd;

                var x = new List<int>(pointCount) { x0 };
                var y = new List<int>(pointCount) { y0 };
                foreach (var delta in xDeltas) {
                    x.Add(x[x.Count - 1] + delta);
                }
                foreach (var delta in yDeltas) {
                    y.Add(y[y.Count - 1] + delta);
                }

                var pressure0 = ReadU16(payload, ref offset);
                var pressureLength = checked((int) ReadU32(payload, ref offset));
                var pressureEnd = CheckedEnd(offset, pressureLength, payload.Length, "pressure stream");
                var pressureDeltas = DecodeDeltaRle(payload, offset, pressureEnd - offset, pointCount - 1);
                offset = pressureEnd;

                var pressure = new List<int>(pointCount) { pressure0 };
                foreach (var delta in pressureDeltas) {
                    var next = pressure[pressure.Count - 1] + delta;
                    if (next < 0 || next > 1023) {
                        throw new ZpeInkException("pressure out of range");
                    }
                    pressure.Add(next);
                }

                var tilt = Repeat(0, pointCount);
                if (hasTilt) {
                    var tilt0 = ReadI16(payload, ref offset);
                    var tiltLength = checked((int) ReadU32(payload, ref offset));
                    var tiltEnd = CheckedEnd(offset, tiltLength, payload.Length, "tilt stream");
                    var tiltDeltas = DecodeDeltaRle(payload, offset, tiltEnd - offset, pointCount - 1);
                    offset = tiltEnd;

                    tilt = new List<int>(pointCount) { tilt0 };
                    foreach (var delta in tiltDeltas) {
                        var next = tilt[tilt.Count - 1] + delta;
                        if (next < -900 || next > 900) {
                            throw new ZpeInkException("tilt out of range");
                        }
                        tilt.Add(next);
                    }
                }

                var azimuth = Repeat(0, pointCount);
                if (hasAzimuth) {
                    var azimuth0 = ReadI16(payload, ref offset);
                    var azimuthLength = checked((int) ReadU32(payload, ref offset));
                    var azimuthEnd = CheckedEnd(offset, azimuthLength, payload.Length, "azimuth stream");
                    var azimuthDeltas = DecodeDeltaRle(payload, offset, azimuthEnd - offset, pointCount - 1);
                    offset = azimuthEnd;

                    azimuth = new List<int>(pointCount) { azimuth0 };
                    foreach (var delta in azimuthDeltas) {
                        var next = azimuth[azimuth.Count - 1] + delta;
                        if (next < 0 || next > 3600) {
                            throw new ZpeInkException("azimuth out of range");
                        }
                        azimuth.Add(next);
                    }
                }

                strokes.Add(new ZpeInkStroke(x, y, pressure, tilt, azimuth));
            }

            if (offset != payload.Length) {
                throw new ZpeInkException("payload contains trailing bytes");
            }

            return new ZpeInkDecoded("ZPINK", header.Version, mode, header.Flags, header.Seed, strokes);
        }

        public static string DecodeToCanonicalJson(byte[] bytes) {
            return Decode(bytes).CanonicalJson();
        }

        private static string ModeName(byte code) {
            switch (code) {
                case 0:
                    return "lossless";
                case 1:
                    return "high";
                case 2:
                    return "medium";
                case 3:
                    return "sketch";
                default:
                    throw new ZpeInkException("invalid mode code: " + code);
            }
        }

        private static List<int> Repeat(int value, int count) {
            var output = new List<int>(count);
            for (var i = 0; i < count; i++) {
                output.Add(value);
            }
            return output;
        }

        private static int CheckedEnd(int offset, int length, int total, string label) {
            long end = (long) offset + length;
            if (end > total || end < offset) {
                throw new ZpeInkException(label + " length overflows payload");
            }
            return (int) end;
        }

        private static List<int> DecodeDeltaRle(byte[] data, int offset, int length, int count) {
            if (count == 0) {
                return new List<int>();
            }

            var end = CheckedEnd(offset, length, data.Length, "delta stream");
            var values = new List<int>(count);
            var cursor = offset;
            while (values.Count < count) {
                if (cursor >= end) {
                    throw new ZpeInkException("delta stream ended before expected count");
                }

                var deltaEncoded = DecodeVarUInt(data, ref cursor, end);
                var run = DecodeVarUInt(data, ref cursor, end);
                if (run == 0) {
                    throw new ZpeInkException("delta stream contains zero-length run");
                }

                var delta = ZigzagDecode(deltaEncoded);
                for (var i = 0; i < run; i++) {
                    values.Add(delta);
                    if (values.Count > count) {
                        throw new ZpeInkException("delta stream run lengths overflow point count");
                    }
                }
            }

            if (cursor != end) {
                throw new ZpeInkException("delta stream has trailing bytes");
            }
            return values;
        }

        private static uint DecodeVarUInt(byte[] data, ref int offset, int limit) {
            uint value = 0;
            var shift = 0;
            while (offset < limit) {
                var chunk = data[offset++];
                value |= (uint) (chunk & 0x7F) << shift;
                if ((chunk & 0x80) == 0) {
                    return value;
                }
                shift += 7;
                if (shift > 35) {
                    throw new ZpeInkException("varuint overflow");
                }
            }
            throw new ZpeInkException("unexpected end of stream while decoding varuint");
        }

        private static int ZigzagDecode(uint value) {
            return (int) (value >> 1) ^ -((int) (value & 1));
        }

        private static ushort ReadU16(byte[] data, ref int offset) {
            if (offset + 2 > data.Length) {
                throw new ZpeInkException("unexpected end of payload (u16)");
            }
            var value = (ushort) (data[offset] | (data[offset + 1] << 8));
            offset += 2;
            return value;
        }

        private static short ReadI16(byte[] data, ref int offset) {
            return unchecked((short) ReadU16(data, ref offset));
        }

        private static uint ReadU32(byte[] data, ref int offset) {
            if (offset + 4 > data.Length) {
                throw new ZpeInkException("unexpected end of payload (u32)");
            }
            uint value = (uint) data[offset]
                | ((uint) data[offset + 1] << 8)
                | ((uint) data[offset + 2] << 16)
                | ((uint) data[offset + 3] << 24);
            offset += 4;
            return value;
        }

        private static int ReadI32(byte[] data, ref int offset) {
            return unchecked((int) ReadU32(data, ref offset));
        }

        private static uint Crc32(byte[] data) {
            uint crc = 0xFFFF_FFFF;
            for (var i = 0; i < data.Length; i++) {
                crc ^= data[i];
                for (var bit = 0; bit < 8; bit++) {
                    if ((crc & 1) == 1) {
                        crc = (crc >> 1) ^ 0xEDB8_8320;
                    } else {
                        crc >>= 1;
                    }
                }
            }
            return ~crc;
        }
    }
}
