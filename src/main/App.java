package src.main;

public class App {

    public static int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {

        while(true){
            System.out.println("Application Running");

            try{
                Thread.sleep(5000);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }
}