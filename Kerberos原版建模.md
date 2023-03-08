# Kerberos原版建模

```spdl
usertype Sessionkey;
usertype Text;
const pk:Function;
secret ktk,sk,k: Function;
secret kck: Function;
secret kst: Function;
usertype timestamp;

protocol kerberos(C,AS,TGS,S) {

	role C {
		fresh n1: Nonce;
		fresh n2: Nonce;
        fresh tm2:timestamp;
        fresh tm4:timestamp;
        fresh t: Text;
		var tgt: Ticket;
		var st: Ticket;
		var AKey: Sessionkey;
		var SKey: Sessionkey;
		
        var tm1:timestamp;
        var tm3:timestamp;
              
		send_1(C,AS,C,TGS,n1);
        recv_!tm1(AS,C,tm1);
		recv_2(AS,C, tgt, { AKey,n1,TGS ,tm1}k(C) );

		claim(C,Running,TGS,tm2);

		send_!tm2(C,AS,tm2);
		send_3(C,TGS, tgt, { C ,tm2}AKey,C,S,n2 );
        recv_!tm3(TGS,C,tm3);
		recv_4(TGS,C, C, st, { SKey, n2, S ,tm3}AKey );
		
		send_!tm4(C,S,tm4);
		send_5(C,S, st, { C,t,tm4 }SKey );
		recv_6(S,C,{t,tm4}SKey );


        claim(C,Nisynch);
		
		claim(C,Secret,AKey);
        claim(C, Secret, SKey);
                
	}
	role AS {
		var n1: Nonce;
		fresh AKey: Sessionkey;
        fresh tm1:timestamp;
                
		recv_1(C,AS,C,TGS,n1);

        send_!tm1(AS,C,tm1);

		send_2(AS,C, { AKey, C,tm1 }k(TGS), { AKey,n1,TGS ,tm1}k(C) );
	
        claim(AS,Nisynch);
		claim_AS1(AS,Secret,AKey);
                
	}

	role TGS {
		var AKey: Sessionkey;
		var n2: Nonce;
        var tm1:timestamp;
        var tm2:timestamp;
		fresh SKey: Sessionkey;
        fresh tm3:timestamp;
                
        recv_!tm2(C,TGS,tm2);

		recv_3(C,TGS, { AKey, C ,tm1}k(TGS), { C ,tm2}AKey,C,S,n2 );
                send_!tm3(TGS,C,tm3);
		send_4(TGS,C, C,{ SKey, C,tm3}k(S), { SKey, n2, S,tm3 }AKey );
               //claim(TGS,Nisynch);
		claim(TGS,Commit,C,tm2);
		claim(TGS,Secret,AKey);

		// My own

		claim(TGS,Secret,SKey);
                 
	}
	role S {
		var t: Text;
		var SKey: Sessionkey;
        var tm3:timestamp;
        var tm4:timestamp;
        recv_!tm4(C,S,tm4);
		recv_5(C,S, { SKey, C,tm3 }k(S), { C,t,tm4 }SKey );
		send_6(S,C, { t,tm4}SKey );

		// My own
        //claim(S,Nisynch);
		claim(S, Secret, t);
		claim(S, Secret, SKey);
                
	}
}


```

![image-20221111202005234](C:\Users\13392\AppData\Roaming\Typora\typora-user-images\image-20221111202005234.png)

![image-20221110225937312](C:\Users\13392\AppData\Roaming\Typora\typora-user-images\image-20221110225937312.png)

保密性分析：



![pattern-kerberos_TGS_TGS3-68](E:\Drops\Typora\图片\pattern-kerberos_TGS_TGS3-68.png)







Kerberos消息完整性：



![pattern-kerberos_TGS_TGS1-32](E:\Drops\Typora\图片\pattern-kerberos_TGS_TGS1-32.png)

认证性分析：



![pattern-kerberos_C_C2-3](E:\Drops\Typora\图片\pattern-kerberos_C_C2-3.png)

消息Recv_3:Dave→Bob {SKey#1,Dave,tm3#1]k(Alice),[SKey#1,IntruderNoncel,Alice,tm3#1}IntruderSessionkey 1