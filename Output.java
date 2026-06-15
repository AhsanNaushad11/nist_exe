import com.grunka.random.fortuna.Fortuna;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Random;


/**
 * Usage examples:
 * For generating a raw file named out0.bin that is 123 MB: java -cp fortuna-2.1.jar Output.java raw 123 out0.bin
 * For generating a scaled file with ints named out_int.txt with 20000 lines with values from 100 (inclusive) to 900000 (exclusive): java -cp fortuna-2.1.jar Output.java scaledInt 20000 100 900000 out_int.txt
 * For generating a scaled file with longs named out_long.txt with 10000 lines with values from 0 (inclusive) to 500000 (exclusive): java -cp fortuna-2.1.jar Output.java scaledLong 10000 0 500000 out_long.txt
 */
void main(String[] args) {
    if (args.length == 3 && "raw".equals(args[0])) {
        int megaBytes = Integer.parseInt(args[1]);
        Random fortuna = Fortuna.createInstance();
        try (OutputStream output = Files.newOutputStream(Path.of(args[2]), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            byte[] bytes = new byte[1024 * 1024];
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
    if (args.length == 5 && "scaledInt".equals(args[0])) {
        int lines = Integer.parseInt(args[1]);
        int min =  Integer.parseInt(args[2]);
        int max = Integer.parseInt(args[3]);
        Random fortuna = Fortuna.createInstance();
        try (BufferedWriter writer = Files.newBufferedWriter(Path.of(args[4]), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            for (int i = 0; i < lines; i++) {
                writer.write(fortuna.nextInt(min, max) + "\n");
            }
        } catch (IOException e) {
            System.err.println("Failed to write to file " + args[4]);
            e.printStackTrace(System.err);
            System.exit(1);
        }
        return;
    }
    if (args.length == 5 && "scaledLong".equals(args[0])) {
        int lines = Integer.parseInt(args[1]);
        long min =  Long.parseLong(args[2]);
        long max = Long.parseLong(args[3]);
        Random fortuna = Fortuna.createInstance();
        try (BufferedWriter writer = Files.newBufferedWriter(Path.of(args[4]), StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            for (int i = 0; i < lines; i++) {
                writer.write(fortuna.nextLong(min, max) + "\n");
            }
        } catch (IOException e) {
            System.err.println("Failed to write to file " + args[4]);
            e.printStackTrace(System.err);
            System.exit(1);
        }
        return;
    }
    System.err.println("See comment at top of this file for usage");
    System.exit(1);
}
