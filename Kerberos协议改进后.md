# Kerberos协议改进后

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
		recv_2(AS,C, tgt, { AKey,n1,TGS ,tm1}kck(C,AS) );

		claim(C,Running,TGS,tm2);

		send_!tm2(C,TGS,tm2);
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

		send_2(AS,C, { AKey, C,tm1 }ktk(AS,TGS), { AKey,n1,TGS ,tm1}kck(C,AS) );
	
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

		recv_3(C,TGS, { AKey, C ,tm1}ktk(AS,TGS), { C ,tm2}AKey,C,S,n2 );
        send_!tm3(TGS,C,tm3);
		send_4(TGS,C, C,{ SKey, C,tm3}kst(TGS,S), { SKey, n2, S,tm3 }AKey );
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
		recv_5(C,S, { SKey, C,tm3 }kst(TGS,S), { C,t,tm4 }SKey );
		send_6(S,C, { t,tm4}SKey );

		// My own
        //claim(S,Nisynch);
		claim(S, Secret, t);
		claim(S, Secret, SKey);
                
	}
}


```



![image-20221111220636265](C:\Users\13392\AppData\Roaming\Typora\typora-user-images\image-20221111220636265.png)





![pattern-kerberos_C_C2-1](E:\Drops\Typora\图片\pattern-kerberos_C_C2-1.png)

Kerberos协议本身就有安全性能高的优点，由于引人了动态口令机制中的时间同步机制，该协议能够防范重放攻击，通过该协议能够证实票据使用者与票据所有者的一致性，因此该协议也能防范冒充攻击、中间人攻击等常见攻击。但是Kerberos协议存在易受到口令攻击的缺陷，而KDH协议能够解决该缺陷，并且不产生其他安全缺陷。

首先，KDH协议能解决Kerberoe易受到口令攻击的缺陷。对于离线口令猜测攻击，在客户与认证服务器进行认证的过程中，用到了Die-Hellman密钥协商，采用强密钥KDH代替原Kerberos协议中的弱密钥K.进行加密，这样就达到了防范离线口令猜测攻击的目的。