namespace FlagPrinter
{
    using System;
    using System.Runtime.InteropServices;

    /// <summary>Contains native method declarations.</summary>
    internal static class NativeMethods
    {
        /// <summary>Checks the validity of the specified password.</summary>
        /// <param name="password">The password to validate.</param>
        /// <returns>0 if the password is valid, otherwise non-zero.</returns>
        [DllImport("PasswordValidation")]
        internal static extern int IsPasswordValid(string password);
    }

    /// <summary>Contains the main entry point of the application.</summary>
    public class Program
    {
        /// <summary>The flag for the challenge :)</summary>
        private const string Flag = "";  // not that easy...

        /// <summary>Main entry point of the application.</summary>
        public static void Main()
        {
            while (true)
            {
                // read the user's password from stdin
                Console.Write("Enter password: ");
                var password = Console.ReadLine();

                // validate it using the secure authentication library
                Console.Write("Authentication: ");
                if (NativeMethods.IsPasswordValid(password) == 0)
                {
                    // the password was authenticated successfully
                    Console.WriteLine("ACCEPTED!\n");
                    break;
                }

                // the password was rejected
                Console.WriteLine("REJECTED!\n");
            }

            Console.WriteLine("Congratulations!");
            Console.WriteLine("The flag is \"{0}\".", Flag);
            Console.ReadKey();  // don't quit until after a key is pressed
        }
    }
}
