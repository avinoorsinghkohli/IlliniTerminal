public class UtilityClass {
    
    public static String formatString(String input) {
        return input != null ? input.trim().toUpperCase() : null;
    }

    public static int calculateSum(int a, int b) {
        return a + b;
    }

    public static boolean isNullOrEmpty(String str) {
        return str == null || str.isEmpty();
    }

    public static String concatenateStrings(String... strings) {
        StringBuilder result = new StringBuilder();
        for (String str : strings) {
            if (str != null) {
                result.append(str);
            }
        }
        return result.toString();
    }
}