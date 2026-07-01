import com.grunka.random.fortuna.Fortuna;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Random;

/**
 * CLI tool for generating cryptographically secure random data using the
 * Fortuna CSPRNG.
 *
 * <p>
 * Supports three output modes:
 * </p>
 * <ul>
 * <li><b>raw</b> — writes raw binary bytes to a file (size specified in
 * megabytes)</li>
 * <li><b>scaledInt</b> — writes random {@code int} values within [min, max) to
 * a text file, one per line</li>
 * <li><b>scaledLong</b>— writes random {@code long} values within [min, max) to
 * a text file, one per line</li>
 * </ul>
 *
 * <p>
 * <b>Usage examples:</b>
 * </p>
 * 
 * <pre>
 *   java -cp fortuna-2.1.jar Output.java raw 123 out0.bin
 *   java -cp fortuna-2.1.jar Output.java scaledInt 20000 100 900000 out_int.txt
 *   java -cp fortuna-2.1.jar Output.java scaledLong 10000 0 500000 out_long.txt
 * </pre>
 *
 * <p>
 * Requires Java 21+ (uses JEP 463 implicitly declared classes and instance main
 * methods).
 * </p>
 *
 * @see com.grunka.random.fortuna.Fortuna
 */
public class Output_modified {
    public static void main(String[] args) {
        // --- Mode 1: Raw binary output ---
        if (args.length == 3 && "raw".equals(args[0])) {
            // REVIEW: No validation that megaBytes > 0. A negative or zero value silently
            // produces an empty file.
            int megaBytes = Integer.parseInt(args[1]);
            Random fortuna = Fortuna.createInstance();
            try (OutputStream output = Files.newOutputStream(Path.of(args[2]), StandardOpenOption.CREATE,
                    StandardOpenOption.TRUNCATE_EXISTING)) {
                byte[] bytes = new byte[1024 * 1024]; // 1 MB buffer
                // BUG: nextBytes() is called ONCE, outside the loop. Every megabyte written to
                // the
                // output file is an identical copy of the same 1 MB block. For randomness
                // testing
                // (e.g. NIST STS), this will produce catastrophically biased results.
                // FIX: Move fortuna.nextBytes(bytes) inside the for-loop so each block is
                // unique.
                fortuna.nextBytes(bytes);
                for (int i = 0; i < megaBytes; i++) {
                    output.write(bytes);
                }
            } catch (IOException e) {
                System.err.println("Failed to write to file " + args[2]);
                e.printStackTrace(System.err);
                System.exit(1);
            }
            return;
        }
        // --- Mode 2: Scaled integer output ---
        if (args.length == 5 && "scaledInt".equals(args[0])) {
            // REVIEW: No validation that lines > 0 or that min < max.
            // If min >= max, Fortuna.nextInt(min, max) will throw IllegalArgumentException
            // at runtime.
            int lines = Integer.parseInt(args[1]);
            int min = Integer.parseInt(args[2]);
            int max = Integer.parseInt(args[3]);
            Random fortuna = Fortuna.createInstance();
            try (BufferedWriter writer = Files.newBufferedWriter(Path.of(args[4]), StandardOpenOption.CREATE,
                    StandardOpenOption.TRUNCATE_EXISTING)) {
                for (int i = 0; i < lines; i++) {
                    // NOTE: String concatenation in a tight loop creates a temporary String per
                    // iteration.
                    // For very large line counts, consider using writer.write(String.valueOf(...))
                    // + writer.newLine().
                    writer.write(fortuna.nextInt(min, max) + "\n");
                }
            } catch (IOException e) {
                System.err.println("Failed to write to file " + args[4]);
                e.printStackTrace(System.err);
                System.exit(1);
            }
            return;
        }
        // --- Mode 3: Scaled long output ---
        // REVIEW: This block is nearly identical to the scaledInt block above. Consider
        // extracting a shared helper method to reduce duplication and simplify future
        // maintenance.
        if (args.length == 5 && "scaledLong".equals(args[0])) {
            // REVIEW: Same validation gap as scaledInt — no check that lines > 0 or min <
            // max.
            int lines = Integer.parseInt(args[1]);
            long min = Long.parseLong(args[2]);
            long max = Long.parseLong(args[3]);
            Random fortuna = Fortuna.createInstance();
            try (BufferedWriter writer = Files.newBufferedWriter(Path.of(args[4]), StandardOpenOption.CREATE,
                    StandardOpenOption.TRUNCATE_EXISTING)) {
                for (int i = 0; i < lines; i++) {
                    writer.write(fortuna.nextLong(min, max) + "\n");
                }
            } catch (IOException e) {
                StringBuilder stringBuilder = new StringBuilder();
                stringBuilder.append("Failed to write to file ");
                stringBuilder.append(args[4]);
                System.err.println(stringBuilder.toString());
                e.printStackTrace(System.err);
                System.exit(1);
            }
            return;
        }
        // REVIEW: Directing users to read source code comments is not ideal UX.
        // Consider printing the actual usage synopsis to stderr here.
        System.err.println("See comment at top of this file for usage");
        System.exit(1);
    }
}
