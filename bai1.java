import java.util.Scanner;

// Lớp Người
class Person {
    protected String hoTen;
    protected int namSinh;
    protected String diaChi;

    public Person() {
        hoTen = "";
        namSinh = 0;
        diaChi = "";
    }

    public Person(String hoTen, int namSinh, String diaChi) {
        this.hoTen = hoTen;
        this.namSinh = namSinh;
        this.diaChi = diaChi;
    }
    public Person(Person d){
        this.hoTen=d.hoTen;
        this.namSinh=d.namSinh;
        this.diaChi=d.diaChi;
    }
    public void input() {
        Scanner sc = new Scanner(System.in);
        System.out.print("Nhập họ tên: ");
        hoTen = sc.nextLine();
        System.out.print("Nhập năm sinh: ");
        namSinh = sc.nextInt();
        sc.nextLine(); 
        System.out.print("Nhập địa chỉ: ");
        diaChi = sc.nextLine();
        sc.close();
    }

    public void output() {
        System.out.println("Họ tên: " + hoTen);
        System.out.println("Năm sinh: " + namSinh);
        System.out.println("Địa chỉ: " + diaChi);
    }
}

class Student extends Person {
    private String lop;
    private double diemTB;

    public Student() {
        super();
        lop = "";
        diemTB = 0;
    }

    public Student(String hoTen, int namSinh, String diaChi, String lop, double diemTB) {
        super(hoTen, namSinh, diaChi);
        this.lop = lop;
        this.diemTB = diemTB;
    }

  
    public void input() {
        super.input(); 
        Scanner sc = new Scanner(System.in);
        System.out.print("Nhập lớp: ");
        lop = sc.nextLine();
        System.out.print("Nhập điểm trung bình: ");
        diemTB = sc.nextDouble();
    }

    // Xuất thông tin học sinh
    public void output() {
        super.output(); // xuất họ tên, năm sinh, địa chỉ
        System.out.println("Lớp: " + lop);
        System.out.println("Điểm trung bình: " + diemTB);
    }
}


public class bai1 {
    public static void main(String[] args) {
        Student hs = new Student();
        hs.input();  
        hs.output();  
    }
}