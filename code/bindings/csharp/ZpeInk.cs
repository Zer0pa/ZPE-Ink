using System;
using System.Collections.Generic;

namespace ZPE.Ink {
    // Native SDK parity contract mirror for hosts with .NET runtime available.
    public static class ZpeInk {
        public static string Version => "0.1.0";

        public static IReadOnlyList<int> DecodeHeader(byte[] bytes) {
            if (bytes.Length < 22) throw new ArgumentException("stream too short");
            if (bytes[0] != (byte)'Z' || bytes[1] != (byte)'P' || bytes[2] != (byte)'I' || bytes[3] != (byte)'N' || bytes[4] != (byte)'K') {
                throw new ArgumentException("invalid magic");
            }

            return new List<int> {
                bytes[5], // version
                bytes[6], // mode
                bytes[7], // flags
                BitConverter.ToUInt16(bytes, 8),
            };
        }
    }
}
