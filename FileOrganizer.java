import java.io.*;
import java.util.Scanner;

/**
 * Created by oyku_ on 2/10/2017.
 school GP-0 MS-1
 sex F-0 M-1
 age numeric
 add U-0 R-1
 famsize LE3-0 GT3-1
 Pstatus T-0 A-1
 Medu numeric
 Fedu numeric
 Mjob T,H,S,A,O
 Fjob T,H,S,A,O
 reason H,R,C,O
 guardian M,F,O
 traveltime numeric
 studytime numeric
 failures numeric
 schoolsup Y-1 N-0
 famsup Y-1 N-0
 paid Y-1 N-0
 activities Y-1 N-0
 nursery Y-1 N-0
 higher Y-1 N-0
 internet Y-1 N-0
 romantic Y-1 N-0
 famrel - numeric
 freetime numeric
 goout - numeric
 Dalc - numeric
 Walc - numeric
 health - numeric
 absences - numeric
 G1 - numeric
 G2 - numeric
 G3 - numeric
 */
public class FileOrganizer {
    public static void main(String args[]){

        Scanner reader;
        FileInputStream input;
        FileWriter writer;
        try {
            input = new FileInputStream("files/student.txt");
            reader = new Scanner(input,"UTF-8");
            writer = new FileWriter(new File("files/studentTest.txt"));
            String line = reader.nextLine(); // no need for the first line with the attribute names
            while(reader.hasNextLine()){
                line = reader.nextLine();
                String token;
                for(int i=0; i<46; i++){
                    if(line.indexOf(";")!=-1) token= line.substring(0,line.indexOf(";"));
                    else token = line;
                    switch(i){
                        case 0: if(token.equals("GP")) writer.write("0,"); else writer.write("1,"); break;
                        case 1: if(token.equals("F")) writer.write("0,"); else writer.write("1,"); break;
                        case 3: if(token.equals("U")) writer.write("0,"); else writer.write("1,"); break;
                        case 4: if(token.equals("LE3")) writer.write("0,"); else writer.write("1,"); break;
                        case 5: if(token.equals("T")) writer.write("0,"); else writer.write("1,"); break;
                        case 15:
                        case 16:
                        case 17:
                        case 18:
                        case 19:
                        case 20:
                        case 21:
                        case 22:if(token.equals("N")) writer.write("0,"); else writer.write("1,"); break;
                        case 8:
                        case 9:if(token.equals("T")) writer.write("1,0,0,0,0,");
                                else if(token.equals("H")) writer.write("0,1,0,0,0,");
                                else if(token.equals("S")) writer.write("0,0,1,0,0,");
                                else if(token.equals("A")) writer.write("0,0,0,1,0,");
                                else writer.write("0,0,0,0,1,"); break;
                        case 10:if(token.equals("H")) writer.write("1,0,0,0,");
                                else if(token.equals("R")) writer.write("0,1,0,0,");
                                else if(token.equals("C")) writer.write("0,0,1,0,");
                                else writer.write("0,0,0,1,"); break;
                        case 11:if(token.equals("M")) writer.write("1,0,0,");
                                else if(token.equals("F")) writer.write("0,1,0,");
                                else writer.write("0,0,1,"); break;
                        case 2:
                        case 6:
                        case 7:
                        case 12:
                        case 13:
                        case 14:
                        case 23:
                        case 24:
                        case 25:
                        case 26:
                        case 27:
                        case 28:
                        case 29:writer.write(token+","); break;
                        case 30:
                        case 31:writer.write(token.substring(1,token.length()-1)+","); break;
                        case 32:writer.write(token); break;
                    }
                    line= line.substring(line.indexOf(";")+1);
                }
                writer.write("\n");
            }
            input.close();
            writer.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        catch (IOException e) {
            e.printStackTrace();
        }



    }
}
