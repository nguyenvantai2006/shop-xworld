import java.util.Scanner;


class Point {
    protected int x;
    protected int y;

    public Point() {
        x = 0;
        y = 0;
    }

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void input() {
        Scanner sc = new Scanner(System.in);
        System.out.print("Nhập hoành độ x: ");
        x = sc.nextInt();
        System.out.print("Nhập tung độ y: ");
        y = sc.nextInt();
    }

    public void output() {
        System.out.println("Điểm (" + x + ", " + y + ")");
    }
}


class ColorPoint extends Point {
    private int color; 

    public ColorPoint() {
        super();
        color = 0;
    }

    public ColorPoint(int x, int y, int color) {
        super(x, y);
        this.color = color;
    }

   
    public void input() {
        super.input();
        Scanner sc = new Scanner(System.in);
        System.out.print("Nhập màu (dạng số nguyên): ");
        color = sc.nextInt();
    }

   
    public void output() {
        super.output(); 
        System.out.println("Màu: " + color);
    }
}


public class bai2 {
    public static void main(String[] args) {
        ColorPoint p = new ColorPoint();
        p.input();  
        p.output();  
    }
}