import java.util.Scanner;
class DV{
    protected String ten;
    protected String mau;
    public DV(){
        ten="";
        mau="";
    }
    public DV(String ten,String mau){
        this.ten=ten;
        this.mau=mau;
    }
    public DV(DV d){
        this.ten=d.ten;
        this.mau=d.mau;
    }
    public void imput(){
        Scanner sc=new Scanner(System.in);
        System.out.println("nhap ten cho meo");
        ten=sc.nextLine();
        System.out.println("nhap mau cho meo");
        mau=sc.nextLine();
        sc.close();
    }
    public void output(){
       System.out.println("ten "+ten);
       System.out.println("mau "+mau);
    }
}
class meo extends DV{
    private String keu;
    public meo(){
        keu="";
    }
    public meo(String keu){
        this.keu=keu;
    }
    public meo(meo m){
        this.keu=m.keu;
    }
}
public class bai3 {
     public static void main(String[] args) {
        meo mo=new meo();
        mo.imput();
        mo.output();
     }
    
}