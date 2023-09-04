import unittest
from scanner import scanner, filterFormatTokens, trasformsTokens
from parser2 import Parser

class ParserTests(unittest.TestCase):
    # def test_parser(self):
    #     testCode = '''
    #     void main (void){}
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))


    # def test_parser2(self):
    #     testCode = '''
    #     int testFun(int nums []){
    #     int a;
    #     int b;
    #     a = a + 1;
    #     if (a < b) {
    #     b = b * a;
    #     }
    #     }

    #     void main (void){
    #     int nums [3];
    #     testFun(nums)
    #     }
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))


    # def test_parser3(self):
    #     testCode = '''
    #     int funcCount(void) {
    #         int total = 0;
    #         while (count < 10) {
    #             if (count <= 2) {
    #                 total + count;
    #             } else {
    #                 total - count;
    #             }
    #             count + 1;
    #         }
    #         return 0;
    #     }
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))
    
    # def test_parser4(self):
    #     testCode = '''
    #     int funcCount(void) {
    #     }
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))


    # def test_parser5(self):
    #     testCode = '''
    #     /* Program that reads a 10 element array of 
    #     integers, and then multiply each element of 
    #     the array by a float, stores the result into an 
    #     array of floats. Subsequently, the array of 
    #     floats is sorted and display it into standard 
    #     output.*/

    #     int x[10];
    #     string s;
    #     float f1;
    #     float f2[10];

    #     int miniloc(float a[], int low, int high){
    #         int i; 
    #         float y; 
    #         int k;

    #         k = low;
    #         y = a[low];
    #         i = low + 1;
    #         while (i < high){
    #             if (a[i] < x){
    #                 y = a[i];
    #                 k = i;
    #             }
    #             i = i + 1;
    #         }
    #         return k;
    #     }/* END of miniloc() */ 
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))
    
    # def test_parser6(self):
    #     testCode = '''
    #     void sort(float a[], int low, int high){
    #         int i; int k;

    #         i = low;
    #         while (i < high - 1){
    #             float t;
    #             k = miniloc(a,i,high);
    #             t = a[k];
    #             a[k] = a[i];
    #             a[i] = t;
    #             i = i +1;
    #         }
    #     return;
    #     }/* END of sort() */
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))


    # def test_parser7(self):
    #     testCode = '''
    #     void readArray(void){
    #         int i; 
    #         s = "Enter a float number: ";
    #         write(s);
    #         read(f1);
    #         while (i < 10){
    #             s = "Enter an integer number: ";
    #             write(s);
    #             read x[i];
    #             f2[i] = x[i]*f1;
    #             i = i + 1;
    #         }
    #         return;
    #     }/* END of readArray() */
    #     '''

    #     # Corre el scanner
    #     tokens = scanner(testCode)

    #     # Filtra y le da formato a los tokens del scanner
    #     filtered_tokens = filterFormatTokens(tokens)

    #     # Trasforma los tokens en un symbol table
    #     transformed_tokens = trasformsTokens(filtered_tokens)

    #     # Crea una instancia del parser
    #     parser = Parser(transformed_tokens[1], transformed_tokens[0])

    #     # Se llama el parser
    #     try:
    #         parser.program()
    #         print("Parsing completed successfully")
    #     except Exception as e:
    #         print("Parsing failed:", str(e))

    def test_parser8(self):
        testCode = '''
       void main(void){
       string s;
s = "Reading Information…..";
input(s);
readArray(); 
s = "Sorting…..";
input(s);
sort(f2,0,10);
s = "Sorted Array:";
output(s);
writeArray();
return;
}/* END of main() */ *
        '''

        # Corre el scanner
        tokens = scanner(testCode)

        # Filtra y le da formato a los tokens del scanner
        filtered_tokens = filterFormatTokens(tokens)

        # Trasforma los tokens en un symbol table
        transformed_tokens = trasformsTokens(filtered_tokens)

        # Crea una instancia del parser
        parser = Parser(transformed_tokens[1], transformed_tokens[0])

        # Se llama el parser
        try:
            parser.program()
            print("Parsing completed successfully")
        except Exception as e:
            print("Parsing failed:", str(e))

if __name__ == '__main__':
    unittest.main()
