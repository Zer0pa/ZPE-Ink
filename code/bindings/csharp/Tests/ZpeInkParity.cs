using System;
using System.IO;
using ZPE.Ink;

public static class ZpeInkParity {
    public static int Main(string[] args) {
        if (args.Length != 2) {
            Console.Error.WriteLine("usage: mono ZpeInkParity.exe <input.zpink> <expected.json>");
            return 2;
        }

        try {
            var input = File.ReadAllBytes(args[0]);
            var expected = File.ReadAllText(args[1]);
            var actual = ZpeInk.DecodeToCanonicalJson(input);
            if (!String.Equals(actual, expected, StringComparison.Ordinal)) {
                Console.Error.WriteLine("csharp parity mismatch");
                return 1;
            }

            Console.Write(actual);
            return 0;
        } catch (Exception ex) {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
    }
}
