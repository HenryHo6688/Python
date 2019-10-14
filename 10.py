第10章 自动化管理进阶：Shell script和Python 3脚本开发实例

对于RHEL 8系统的使用者和管理者而言，最基本的语言就是C了，它可以说是RHEL及其他各种Linux的母语了，系统本身主要就是由C写成的，时至今日，C语言依旧是构建操作系统及底层最为常用的语言，不过由于C语言本身就较为复杂，开发效率也低，反倒不如Shell script来的简单和高效，只要会一些命令即可高效地完成任务，但Shell script毕竟只是bash自身的一个扩展功能，尽管高效但功能上还有一些欠缺，不过对于多数应用场景已经足够了。

如果非要一种计算机语言辅助的话，那非Python莫属了，Python是一种高雅，简洁和高效的语言，《Thinking in Java》及《Thinking in C ++》的作者Bruce Eckel曾说“Life is short ,you need Python(人生苦短，我用Python)”，几十行代码就可以实现C或其他语言数百行的功能，如Ansible，Cobbler，Fabric及Saltstack等流行的自动化工具都是采用Python开发的，这绝非偶然，下面就先易后难，从最容易上手的Shell及Shell script说起。

Shell是所有Linux所共有的一个工具，成功登录后就会执行Shell，那么到底Shell是什么样的工具，其实，Shell对我们来说并不是一个陌生的内容，在第一次进入RHEL的时候已经接触过它了，想必大家对其黑乎乎的面孔记忆犹新，当登录到RHEL 8时(无论是本地登录还是远程登录)所出现的界面，输入用户名和密码后就会进入Shell界面，这也是通常所说的命令行，Shell可以理解为运行命令行的一个容器，但其本身则是夹在操作系统和用户之间的一个程序。

Shell的中文意思是“壳”，它能够提供一个交互环境来使用户和内核进行沟通。众所周知，计算机的任务最终是由硬件来完成的，如听歌要播放CD，这需要使用光驱，听到声音要用到声卡，看到图像要用到显卡和显示器，但是这些硬件自己是不会工作的，需要内核来发出指令来调动它们进行工作（如果内核认不出的话硬件就无法工作了，这也是要安装硬件驱动的原因），但一般人是无法直接对内核进行操作的，只能通过一些工具界面来对其操作，然后下达命令，这样这些工具就来解释所使用的命令并与内核沟通，使内核收到命令后控制相应的硬件进行工作，而Shell正是这样的一个工具。在通常情况下，Shell是成功登录后就开始运行的程序，它能够允许用户在它所提供的命令行界面输入命令，并通过解释这些用户执行的命令来完成用户和内核之间的交互。

至于Shell script则是一门功能极为强大的脚本语言，可以把一些需要经常输入的命令放到一个文件里，然后赋予这个文件可执行权限，运行此文件，这样放在文件里的所有命令会一次性运行。这个文件叫做Shell脚本，它与批处理文件类似，但它的功能要远比一般的批处理文件强得多，因为它提供了一些语言所提供的功能，例如判断、循环等，所以它是一门脚本语言。

绝大多数Linux都不仅仅只支持一种Shell，如果想要知道当前的RHEL中可以支持哪些Shell，可以通过以下方式来查看：
cat /etc/shells
/bin/sh
/bin/bash
/usr/bin/sh
/usr/bin/bash

这样会发现多种Shell可供使用，每个Shell都有自己的一些特点，绝大多数Linux发行版本都是以bash作为默认的Shell，由于bash（Bourne Again Shell）也是RHEL 8的默认Shell，所以下面所有操作均是以bash为准的，其他Shell读者朋友如果感兴趣可以查阅相关手册。

Bash是由Brain Fox在1988年开发的，所有版本均受GNU通用许可证的保护，并且可以自由使用。如果想查看当前的RHEL 8中的Bash的版本，可以通过如下方式：
echo $BASH_VERSION
4.4.19(1)-release

下面就来了解一下bash所提供的三大人性化的功能，命令补齐，命令历史和命令别名。

1．命令(文件或目录名)补齐
由于bash主要是基于命令行操作的，所以绝大多数时间是用键盘进行输入的，但有时候可能会碰到一些比较长的命令，输入起来很不方便，此时就可以使用bash提供的命令补齐功能，它能够输入命令或者文件名的前面的一部分，如两到三个字母，然后按下Tab键，后半部分bash便可自动补齐。

如要打开/etc/redhat-release文件，输入下列命令：
vi /etc/redhat-release

此时可以输入vi命令，然后输入/e后再按Tab键，bash便会自动将文件名补全为/etc/,显然还没有达到要求，这时再输入字母r，按两下Tab键，将出现多个文件，这是由于只输入一个r还无法唯一标记一个文件，随后输入ed，再次按下Tab键便可自己补全，又出现两个文件，输入r便可唯一区别了，这样便可自动补全了。如果当前目录下只有一个以r开头的文件或者目录时，系统会自动帮助我们把文件名后面缺少的部分补全。但如果bash一直无法自动补全，说明此目录下真的没有这个的文件了(多数情况是输入错误造成的)。

2．命令历史功能
如果需要输入刚刚输入的命令，可以使用Shell提供的命令历史功能，只需使用上下键来即可显示曾经执行的指令，这样在命令行上就显示了最近输入的命令，还可以使用history命令来进行查看所有输入的命令，history命令的高频参数如下：
-c: 清除当前Shell里的全部history内容。

退出系统后，Shell会将history中的内容写入当前登录用户的家目录下隐藏文件.bash_history文件中，在此需要提醒大家的是，以后涉及一些可以在命令行上输密码的连线服务或者程序时，尽量不要在命令行上输入密码，因为如果疏忽的话很可能在此文件中将密码泄露。

当需要再次输入的命令后就可以执行它，大家可能看到history命令的查询结果，要重复执行某条命令，关键是要记住命令的序列号，所以可以使用以下方式来进行执行命令：
!6

这样就可以执行序列号为6的命令了，此外对于最近一次输入的命令还可以使用!!来重复执行此命令。

3．命令别名功能
如经常使用同一个长命令，那么前面两个方法还是显得麻烦了些，其实bash还可使用一些比较简单的缩写来代替一个长命令，这就是为命令定义一个别名。在bash中定义命令别名的命令是alias，如为了查看inode方便，可以定义一个li别名，具体方法如下：
cd
vi .bashrc

添加如下配置： 
alias li="ls -ilF"

最后运行如下命令让配置立即生效：
source .bashrc

需要说明的是，在等号两端不要有空格，且命令行及参数最好使用引号括起来，因为bash是以空格为单位区分命令和参数的，如果不加引号的话，很容易发生错误，可以使用alias命令查看是否定义成功。如果成功，就使用ll命令直接以长格式方式查看目录内容了：
li
total 60
 68894882 -rw-------. 1 root root  1440 May 20 11:06 anaconda-ks.cfg
 68896099 drwxr-xr-x. 2 root root     6 Sep  1 11:57 Desktop/
 68896100 drwxr-xr-x. 2 root root     6 Sep  1 11:57 Documents/
101855646 drwxr-xr-x. 2 root root     6 Sep  1 11:57 Downloads/
...

将会发现结果和执行“ls -ilF”命令效果是一样的。这样定义别名，退出bash后别名就会失效，如不想失效就要将上述定义写入.bashrc文件。

说完了定义别名，其实取消一个命令别名也很容易，只需要执行命令：
unalias li

再次运行li命令：
li
bash: li: command not found...
Failed to search for file: Cannot update read-only repo

再使用alias命令查看的话就会发现别名已经删除了，当然如果以前已经写在配置文件中了，也要将文件中的别名定义去掉。如要永久失效，就必须编辑.bashrc文件了，注释掉所设置别名即可。

当然，bash的特点远不只以上几条，比如令bash高效的快捷键，如Ctrl+C可以停止当前的命令，Ctrl+Z可以暂停当前的命令，Ctrl+U可以清空当前命令行的内容，Ctrl+L可以清屏（类似于clear）等，大家可以根据实际使用情况自行总结。

10.1. Shell Script开发必知必会
所谓Shell Script其实就是将一组Linux命令通过一定的逻辑关系，如分支或循环，组织起来，高效地完成系统管理的任务，类似于Dos的批处理的程序，比Dos批处理强大的是，编程的要素，如变量，各种表达式，逻辑结构(顺序，分支，循环)及函数等要素一个都不少，其标准格式如下所示：
cat helloworld.sh		#shell script的扩展名为sh，建议采用规范的命名
#!/bin/bash				#Shebang(sha-bang)符号是shell script脚本第一行的固定格式，用于指定执行这个脚本的解释程序，井号和叹号必须连接在一起，后跟解释器bash的绝对路径
echo "Hello world!"		#脚本内容，shell script脚本内容和C或其他语言的文件一样，由多个语句构成

shell script的注释和Python相同，井号后的内容为注释内容，保存退出后还需为脚本添加可执行权限，具体操作如下：
chmod +x helloworld.sh

否则就是一个ASCII文件。上述脚本十分简单，只有一个命令，不过工作中的脚本大多由多个语句构成，脚本也可以定义变量和函数，逻辑结构也是三种，即顺序，分支和循环。此外，脚本也需要调试和测试，没有问题方可使用，下面先从最简单的变量开始学习。

Tips：其他执行shell script的法方法
创建脚本后，除了添加可执行权限运行之外，还可以使用如下两种方法直接运行：
source helloworld.sh

或：
. helloworld.sh				#西文句点

Shell Script的变量
对于学习过某些编程语言的朋友来说，变量并不陌生，它就是使用一些简单的或者有意思的字符来代替一些比较冗长的或者无意义的经常变化的内容，如常见的PATH变量，其实这就是一个环境变量，它记录执行一个命令时命令所要搜寻的路径，还有登录后，主机名显示在了界面上，这也是一个环境变量，系统在启动时读取主机名配置文件（/etc/hostname），然后将其值赋给变量HOSTNAME，最后显示出来，这两个变量可以使用如下命令显示：
echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

echo $HOSTNAME
www.example.com

10.1.1 变量的种类及相关操作
Shell script中的变量虽然很多，但是可以将其分为几类，多数都是系统预设好的，也有的是进行操作时设定的变量，而它们的作用范围也是不一样的。Shell script中的变量分为以下几种：
◆局部变量：只在一定范围内能够使用的变量，只在设定此变量的Shell中有效；
◆环境变量：在整个系统环境中都能使用，不但在设定此变量的bash中有效，而且在由此bash所衍生出的所有子bash中也有效；
◆位置变量：主要用于记录命令及其选项值的变量，是只读的；
◆特殊变量：主要记录一些特殊值的变量，是只读的。

Shell script中变量的操作一定要掌握，如定义取消变量，查看变量，引用变量等，这里所说的变量主要是指局部变量，不过局部变量是可以通过导出的方式变为环境变量的，至于位置变量和特殊变量大多是bash预设好的。

1.定义变量
在bash中定义一个局部变量比较简单，如要定义一个名为NAME变量并且给它赋值为“RHEL”，则可以进行如下操作：
NAME="RHEL"
VERSION="8"

这样就定义好了一个变量，需要注意的是：
◆所定义变量名称规范的写法是全部采用大写字母；
◆定义变量的时候需要用“=”连接，并且等号两边不能有空格；
◆左边是变量名，右边是变量的值，变量的名只能是字母，数字或者下画线，并且不能用数字开头；
◆在一般情况下，用户自定义的变量一般都小写，而系统变量一般都大写。

2．显示(引用)变量的值
设定好了变量后，可以使用echo命令显示它的值：
echo $NAME $VERSION
RHEL 8

echo $LANG
en_US.UTF-8				#可以获得字符编码信息

其中echo命令是用来显示一个变量或字符串的值，而“$”则表示获取变量的值。变量名和变量值其实就是一个对应关系，通过引用变量名而获得变量值。

3．局部变量导出为环境变量
上述NAME变量只是个局部变量，只在当前的bash中是有效的，如果再执行bash命令开启一个子bash的话，则无法使用该变量了：
bash
echo $NAME			#显示变量值为空
			  
而如果要变量在子bash中也生效或是所有用户都能够使用该如何设定？其实只需使用export命令导出即可。export命令可以将在当前bash中设定的变量在以后所有此bash派生出的子bash中都能够使用。还是以刚才的NAME变量为例，在设定NAME变量时直接使用如下命令：
exit						#退出所开启的子bash
export  NAME="RHEL"			#将局部变量导出为环境变量
bash						#再次开启子bash

这样再执行echo命令后，就可以使用NAME变量了。

4．取消变量
变量是要占用一定的内存空间的，所以对于不使用的变量要将它取消，可以使用unset命令，具体操作如下：
unset NAME

这样，当再次使用echo命令查看时就显示为空了。

5．获取当前全部的环境变量
环境变量的定义方法与局部变量是一样的，它们也可以称为全局变量，使用export命令使其在子bash中能使用。需要注意的是，在一个父bash中可以使用export命令导出一个变量给子bash使用，可如果要在子bash中定义一个变量，即使是用export命令导出的，也不能在父bash中使用，而只能向下一级的子bash中传递，也就是说这是个单向的过程。

可以使用env命令能够查看当前所有的环境变量，env命令运行结果如下：
env
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.m4a=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.oga=01;36:*.opus=01;36:*.spx=01;36:*.xspf=01;36:
SSH_CONNECTION=192.168.1.11 62081 192.168.1.168 22
LANG=en_US.UTF-8
HISTCONTROL=ignoredups
DISPLAY=localhost:10.0
HOSTNAME=www.example.com
...

这些变量就是当前bash的环境变量了。

Tips：如何修改命令行默认提示符
Shell可以自定义命令行默认提示符，定义之前，首先需要备份默认的提示符定义，关键操作如下：
echo $PS1 > PS1.bak 

成功执行完该命令就将默认的定义备份到文件PS1.bak了，下面就利用Shell提供的如下颜色代码：
30：白
31：红
32：绿
33：黄
34：蓝
35：紫红
36：青
37：黑

实现彩色提示符，具体操作如下：
PS1='\[\033[0;31m\]\u@\h \W\$\[\033[0m\]'		#[\033[0;31m\]启用指定颜色字符，31代表红色，[\033[0m\]关闭所指定颜色字符，令后续的输入为默认的白色
PS1='\[\033[0;32m\]\u@\h \W\$\[\033[0m\]'
PS1='\[\033[0;33m\]\u@\h \W\$\[\033[0m\]'
PS1='\[\033[0;34m\]\u@\h \W\$\[\033[0m\]'
PS1='\[\033[0;35m\]\u@\h \W\$\[\033[0m\]'
PS1='\[\033[0;36m\]\u@\h \W\$\[\033[0m\]'

看看设置后，提示符就变成彩色的了，还可以定义一些别出心裁的提示符，如：
PS1=					#纯黑脸，没看错，是空值，就是没有提示符
PS1="[\u@\h \w]\$" 		#方括号
PS1="<\u@\h \w>\$" 		#尖括号
PS1="^_^\u@\h \w\$" 	#笑脸

持久化PS1变量，可以将PS1的值直接定义到家目录下的.bashrc文件中，这样PS1就成为默认值了，其他环境变量均可采用这种方法修改，备份，自定义，持久化，举一反三。

10.1.2 位置变量
所谓位置变量就是用来存储所创建脚本名称及需要传递给脚本的参数的变量。位置变量是由它们在作为参数向脚本程序传递过程中的位置区分的，这些位置变量都是只读的，名字是固定的，bash的位置变量如下所示。
◆$0：表示所执行的脚本名称；
◆$(1~9)：代表的是传给程序的参数，分别为$1至$9，从第1个参数到第9个参数；
◆${大于9的数字}：这个含义同上，只是如果位置数要是大于9的话，应该用{}将数字括起。

下面就创建一个脚本来加深理解，脚本名称为script_detail.sh,内容如下：
#!/bin/bash
echo $0
echo $1
echo $2
echo "Shell script name is:$0"
echo "Shell script the first parameter is:$1 "
echo "Shell script the second parameter is:$2 "

保存退出后运行如下命令添加执行权限：
chmod +x script_detail.sh

最后执行脚本，别忘了添加参数哦，具体效果如下：
./script_detail.sh one two
./script_detail.sh
one
two
Shell script name is:./script_detail.sh
Shell script the first parameter is:one
Shell script the second parameter is:two

从结果可知，结果完全正确。

10.1.3 特殊变量
bash不但提供了位置变量，而且还提供很多的特殊变量，这些变量与位置变量一样都是不可变的，这些变量都是由特定字符组合而成，这些变量有的与位置变量有关，有的与bash或命令有关，特殊变量如下所示：
◆$#：表示位置变量的个数；
◆$*：表示所有的位置变量；
◆$@：表示每个位置变量的值；
◆$$：表示当前bash的PID（进程的IP号）的值；
◆$?：最近执行命令的退出值，0表示命令执行成功，非0表示失败。

下面就创建一个脚本，帮助大家记忆，脚本名称为special.sh，该脚本能够将$#，$*，$@等特殊变量显示出来，脚本内容如下：
#!/bin/bash
echo $1 $2
echo $0
echo $#
echo $@
echo $$
echo $?

照例运行如下命令添加可执行权限并运行
chmod +x special.sh
./special.sh 1 2
1 2
./special.sh
2
1 2
1623
0

只需记住这个脚本，只需要运行一下此脚本，这些特殊变量就不容易忘记了，需要注意的是，执行的时候需要加上2个参数，参数和参数之间要用空格分开。

10.1.4 输入和输出语句
和其他编程语言类似，shell script也提供了输入和输出语句，因为这是一个程序最为常用的语句，shell script的输入输出命令为read和echo命令。
◆read命令
read命令可以读取键盘所输入的值，具体使用方法如下：
read CHOICE

随后输入1，再运行输出命令，具体操作如下：
echo $CHOICE
1

可以看到输出的值为1，说明输入输出语句工作正常。

再进一步，如有要使用输入提示如何通过read实现呢？直接使用-p参数和提示信息就可以实现了，具体操作如下：
read -p "Enter your choice:" CHOICE

输入3，随后可以运行如下命令验证：
echo $CHOICE
3

结果正确，还有就是常用的时间限制了，使用-t参数便可实现，具体操作如下：
read -p "Enter your choice:" -t 3 CHOICE

上述命令中-t参数表示bash可以等待的秒数，3表示3秒，即可以等待3秒，如超过这个时间，将进行下一行命令。 

◆echo命令
echo命令可以输出字符串，类似C语言的printf函数的作用，只不过功能没有那么多而言，只能进行简单的输出，此外，echo命令默认是打印换行的，如打印hello world字符串：
echo "hello world"
hello world

直接换行，如果不想换行，可以添加-n参数，具体操作如下：
echo -n "hello world"
hello world[root@www ~]$

除此之外，echo还可以打印出五颜六色的字符串，只需添加-e参数并指定颜色代码即可，具体操作如下：
echo -e "\033[31mhello world\033[0m"

上述命令中，\033[31m表示以红色打印字符串hello world,\033[0m表示关闭颜色输出，关闭颜色输出是必须的，否则默认输出的白色就变为刚指定的颜色了。

Tips：echo实现彩色打印
echo也可以利用Shell提供的颜色代码实现彩色打印的，令黑乎乎的命令行变得漂亮一点，如要打印黄色hello world，可执行如下命令：
echo -e "\033[33mhello world\033[0m"

或创建一个colors.sh的脚本：
#!/bin/bash
echo -e "\033[31mhello world\033[0m"
echo -e "\033[32mhello world\033[0m"
echo -e "\033[33mhello world\033[0m"
echo -e "\033[34mhello world\033[0m"
echo -e "\033[35mhello world\033[0m"
echo -e "\033[36mhello world\033[0m"

运行这个脚本之后，便可看到犹如彩虹一般的hello world字符串了，十分漂亮。

read和echo命令在脚本中经常配合使用，echo命令用来打印菜单的提示信息，read命令则用于读取用户选择，具体实例如下：
echo
echo
echo "+++++++++++++++++++++++++++++"
echo "     1: Print book list	   "
echo "     2：Print book name      "
echo "     3：Print book status    "
echo "     q: Quit                 "
echo "+++++++++++++++++++++++++++++"
read -p"Enter your choice：" CHOICE

执行如下命令读取CHOICE的值：
echo $CHOICE
3

还可以利用单引号，打印特定九九乘法表，实例如下：
cat 9x9.sh
echo '1*1=1'
echo '1*2=2  2*2=4'
echo '1*3=3  2*3=6  3*3=9'
echo '1*4=4  2*4=8  3*4=12 4*4=16'
echo '1*5=5  2*5=10 3*5=15 4*5=20 5*5=25'
echo '1*6=6  2*6=12 3*6=18 4*6=24 5*6=30 6*6=36'
echo '1*7=7  2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49'
echo '1*8=8  2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64'
echo '1*9=9  2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81'

大家可以想想如何使用循环实现九九乘法表的打印，还可以打印更为复杂的图案，只要使用单引号即可，实例如下：
cat iloveu.sh
echo  '              eUIloveUI           IloveUIlo'
echo  '          loveUIloveUIloveU   veUIloveUIloveUIl'
echo  '        IloveUIloveUIloveUIloveUIloveUIloveUIlove'
echo  '       IloveUIloveUIloveUIloveUIloveUIloveUIloveUI'
echo  '      IloveUIloveUIloveUIloveUIloveUIloveUIloveUIlo'
echo  '      loveUIloveUIloveUIloveUIloveUIloveUIloveUIlov'
echo  '      oveUIloveUIloveUIloveUIloveUIloveUIloveUIlove'
echo  '      veUIloveUIloveUIloveUIloveUIloveUIloveUIloveU'
echo  '      eUIloveUIloveUIloveUIloveUIloveUIloveUIloveUI'
echo  '      UIloveUIloveUIloveUIloveUIloveUIloveUIloveUIl'
echo  '       loveUIloveUIloveUIloveUIloveUIloveUIloveUIl'
echo  '        veUIloveUIloveUIloveUIloveUIloveUIloveUIl'
echo  '        eUIloveUIloveUIloveUIloveUIloveUIloveUIlo'
echo  '          loveUIloveUIloveUIloveUIloveUIloveUIl'
echo  '           veUIloveUIloveUIloveUIloveUIloveUIl'
echo  '            UIloveUIloveUIloveUIloveUIloveUIl'
echo  '              oveUIloveUIloveUIloveUIloveUI'
echo  '                UIloveUIloveUIloveUIloveU'
echo  '                  oveUIloveUIloveUIlove'
echo  '                     IloveUIloveUIlo'
echo  '                        eUIloveUI'
echo  '                           ove'
echo  '                            e'

上述实例就是利用单引号的特性打印一个心形图案，还可以使用echo的颜色代码来修饰这个图案。

10.1.5 脚本的逻辑结构
脚本也是支持基本的逻辑结构，如顺序，分支和循环，先从最简单的顺序结构说起，顺序结构基本没什么可说的，就是按照实际执行的顺序将命令写到脚本就可以了，但需要提醒大家的是，顺序结构中的表示方式需要重点掌握，如语句执行顺序控制，输入输出重定向，管道和特殊符号等，先从语句执行顺序说起，有时执行一个命令时，需要另一个命令执行成功或失败后才可以进行，如将/home/test目录移动到/home/bak目录中，再将/home/test目录删除，这样确保目录移动成功后才删除原文件，或需要添加一个用户，但首先确认这个用户不存在才可以，所以先用grep命令在/etc/passwd文件查找一下，如果命令失败才可以执行添加用户的命令，这些都与命令执行的先后顺序有关。命令的执行顺序如下所示：
◆一个命令执行成功后才可以执行另一个命令，可以使用“&&” 来完成；
◆一个命令执行失败后再执行另一个命令，可以使用“||”来完成；
◆如果只是需要连续执行一组命令，可以使用“；”来完成。

以上述移动目录为例子来看一下“&&”的用法，可以执行以下命令：
mkdir /home/bak && cd  /home/bak

或：
mkdir /home/bak && cd  $_					#$_表示所创建的目录

表示mkdir命令执行成功之后，再执行cd切换目录，否则目录无法切换，还可以更加复杂一点，具体操作日如下：
mkdir /home/bak && cd  /home/bak && tar czvf  passwd.tar.gz /etc/passwd /etc/group

这样目录没有创建成功的话，后面的cd就无法执行，更不用说打包了，使用了&&保证了命令的成功执行，但如果换成如下命令：
mkdir /home/bak || cd  /home/bak || tar czvf  passwd.tar.gz /etc/passwd /etc/group

上述命令无论前两个命令成功与否，都会执行打包命令。如果只是希望能够下达多个命令的话，就需要用到“；”隔开，具体操作如下：
mkdir /home/bak ;  cd  /home/bak ;tar czvf  passwd.tar.gz /etc/passwd /etc/group 

还可以将上述命令放在括号中，效果一样，具体操作如下：
(mkdir /home/bak ;  cd  /home/bak ;tar czvf  passwd.tar.gz /etc/passwd /etc/group)

此外，命令替换可以令顺序操作更加便捷，所谓命令替换就是使用一个命令的结构填充另外一个命令，使之能够顺利执行，获得需要的结果，如查看命令mkdir的详细信息，通常的操作为：
which mkdir
/usr/bin/mkdir

获得了mkdir的位置后，再运行：
file /bin/mkdir

比较麻烦，如果使用命令替换符的化，上述操作就可以简化为：
file `which mkdir`				#反引号中的命令会执行

或:
file $(which mkdir)				#等价操作

还有输入输出重定向，在执行一个命令的时候，通常情况下都是从键盘进行输入，然后从屏幕输出结果。如命令执行错误，也会将错误信息显示在屏幕上。在默认情况下，如果不做任何改动，所有这种标准的输入和输出（包括结果和错误）都是按照默认的设备来进行输入输出的。标准输入指的是键盘，标准输出和标准错误输出指的是屏幕。

Linux系统使用的都是标准输入、标准输出和标准错误输出，三者分别使用0（标准输入）、1（标准输出）、2（标准错误输出）表示。如要将命令的结果保存在一个文件里，这就需要用到重定向。重定向指的是将标准输入，标准输出和标准错误的输出由默认变为指定文件或新设备，其中输入的重定向可以使用“<”来完成；输出的重定向可以使用“>”来完成；而标准错误输出的重定向可以使用“2>”来合并到标准输出。如想把每次的结果都保留下来，而不把以前的结果覆盖，使用追加符号“>>”替代原先的“>”即可，将新内容追加到文件的末尾。

如将/etc/passwd文件中的用户名以字母顺序进行排序，然后将排序过后用户列表不显示在屏幕上，而保存在/home/henry/userlist文件中，则可以执行命令：
sort /etc/passwd > $HOME/userlist && cat $HOME/userlist

先使用sort命令将passwd文件内容进行了排序，正常情况下，应该将结果显示在屏幕上，但是由于使用了输出的重定向，这样就将输出的设备由屏幕而改成了文件，因此，将结果保存起来，然后又使用cat命令进行了查看。需要注意的是，原本userlist文件是不存在的，使用输出重定向时，如果文件不存在则创建此文件；如果文件存在的话，则覆盖。

经常使用脚本来完成一些系统管理任务，有时这些脚本都是在后台运行的，这样如果不使用输出重定向保留结果，就无法得知脚本的运行状态，且终端经常会会显示一些错误的提示信息。这就是由于某些脚本在后台运行时发生了一些错误，而并没有使用标准错误输出重定向将错误保存在其他的位置所致。解决此问题的方法是可以使用/dev/null装置，此装置可以将其理解为Linux里的垃圾筒，所有保存到里面的内容都会消失掉。有时只要将标准输出和标准错误输出保存在一个文件中即可，具体操作如下：
tar czvf passwd_bak.tar.gz  /etc/passwd  /etc/group > result  2>&1

上述命令中，将标准输出和标准错误输出都重新定向到了文件result处，因为/group文件并不存在，所以命令执行时会发生一个错误。在此，请读者注意，当标准错误输出与标准输出都是同一个设备时，可以使用“2>&1”来表示，代表标准错误输出与标准输出是同一个位置。

还有先前使用过的管道，也是顺序结构中常用，管道指的是将一个命令的输出作为另外一个命令的输入。先看以下例子：
cat /etc/passwd | wc -l 
46

使用cat命令显示passwd文件的内容，但是并没有显示在屏幕上，而是通过管道“|”变成了另一端的wc命令的输入了，最后显示wc的统计结果，此命令组合实现了统计当前系统内的用户数量。
管道经常和一些文本处理命令进行联合使用，以对文本的处理结果进行处理。

Tips：bash中的特殊字符
在bash中，还有几个符号有着特别的含义，分别是双引号（""）,单引号（''）,$和\,具体说明如下：
◆双引号：双引号内出现的特殊字符（如单引号、$和\）保持原来的含义，并不会被当做普通字符处理；
◆单引号：单引号内出现的特殊字符失去原来的含义，即被当成普通字符来处理；
◆$符号：$的含义为取变量的值，在双引号中，它保持此含义，但是在单引号中，它被作为普通的$字符；
◆\符号：转义字符，即如果一个特殊的字符前面加上了“\”符号，那么此特殊字符就被当成是普通字符处理。

当然，上述这些内容虽然放在了顺序结构中，一旦掌握，用于顺序结构，条件判断和循环结构也是没有问题的。

条件判断
由于分支结构和循环结构中，大概率要用到判断表达式，如文件存在与否，存在执行一个分支，不存在执行另外一个分支，循环中也需要判断表达式，如判断循环条件是否满足等，这些都需要条件判断表达式，所以先来掌握。

在脚本的编写过程中，经常需要作出判断，以决定程序的流程走向。在bash中，使用test命令来完成多数的判断，test命令可以对条件的执行结果进行判断，并且能够返回真（0）或假（非0），如判断/etc/passwd是不是一个普通文件，可以执行如下命令：
test -f /etc/passwd ; echo $?
0

通过test命令判断/etc/passwd文件是否是一个普通文件，如果是，test命令返回结果0，否则返回非0，使用echo命令将其值显示出来，从而能够得到test命令执行结果，返回0，说明/etc/passwd是一个普通文件，这就是一个最简单的判断。test命令的参数非常多，可以使用man test来进行查询，它主要用于检验一个文件类型，文件属性或比较两个值，test命令等价于[],下面就是高频使用的判断参数，使用起来十分简单，根据实例套用就好。

◆对字符串进行判断
string1 = string2								#判断string1是否等于string2，如果相等，返回真
string1 != string2								#判断string1是否不等于string2，如果不等于，返回真
-z string										#判断string长度是否为零，如果为零，返回真
-n string										#判断string长度是否不为零,如果不为零，返回真

◆对整数进行判断
int1 -eq int2									#判断两个整数是否相等，如果相等，返回真
int1 -ne int2									#判断两个整数是否不等，如果不等，返回真
int1 -gt int2 									#判断int1是否大于int2，如果大于，返回真
int1 -ge int2									#判断int1是否大于等于int2，如果是，返回真
int1 -lt int2									#判断int1是否小于int2，如果是，返回真
Int1 -le int2									#判断int1是否小于等于int2，如果是，返回真

◆对文件或类型进行判断
-e 												#判断文件是否存在，如果存在，返回真
-b												#判断文件是否是块设备文件，如果是，返回真
-c 												#判断文件是否是字符设备文件，如果是，返回真
-f 												#判断是否是一个普通文件，如果是，返回真
  
◆对文件或类型进行判断
-d 												#判断是否是一个目录，如果是，返回真
-L												#判断是否是一个链接文件，如果是，返回真

◆对文件属性进行判断
-s 												#判断文件是否是空白文件，如果是，返回真
-r 												#判断文件是否可读，如果是，返回真
-w												#判断文件是否可写，如果是，返回真
-x												#判断文件是否可执行，如果是，返回真
-u												#判断文件是否设置了SUID，如果是，返回真
-g												#判断文件是否设置了SGID，如果是，返回真
-k												#判断文件是否设置了sticky bit属性，如果是，返回真

◆比较两个文件
file1  -nt  file2								#判断file1是否比file2新，如果是，返回真
file1  -ot  file2								#判断file2是否比file1新，如果是，返回真

◆逻辑判断
condition1  -a  condition2						#当condition1(条件)和condition2同时为真时，返回真
condition1  -o  condition2						#当condition1和condition2只要有一个为真，则返回真

下面就使用test命令的上述参数(部分)，判断/etc/passwd文件的相关属性，具体命令如下：
test -e /etc/passwd								#判断文件是否存在

或:
[ -e /etc/passwd ]								#等价于上述命令，下列命令均可采用[]进行替换，分支或循环结构中经常使用，需要注意的是条件前后有两个空格


test ! -e /etc/passwd							#判断文件是否存在,不过返回结果正好相反

或:
[ ! -e /etc/passwd ]							#下列命令均可采用[]进行替换

test -r /etc/passwd								#判断文件是否可读
test -w /etc/passwd 							#判断文件是否可写
test -x /etc/passwd 							#判断文件是否可以执行

test -r /etc/passwd  -a -w /etc/passwd			#将两个判断结果求与
test -r /etc/passwd  -o -w /etc/passwd			#将两个判断结果求或

所有test语句，都可以通过如下命令判断结果：
echo $? 
0												#0表示真，非0表示假

分支结构
在shell script脚本中，经常要使用条件判断语句，最简单的条件语句就是if语句，if语句的语法为：
if [ condition  ]
then 
	command1
	command2
	...
fi
	
需要特别注意的是，if条件语句中空格非常重要，if和“[”之间，条件与左右两边的“[”和“]”之间都要有空格，并且如果then命令要是写在与if相同的一行上，那么应该写成如下格式：
if [ condition ]；then 
	command1
	command2
	...
fi	

if语句执行顺序为当if语句的条件为真时，执行then后的命令，否则不执行命令而直接执行fi后的命令,下面就以login.sh为例来学习if...then语句，对用户输入的名字进行验证，如果输入的是RHEL8，则显示“Hello RHEL8”，否则什么也不显示，脚本内容如下：
cat login.sh
#!/bin/bash											#shebang固定格式，指定脚本的解释器为/bin/bash

read -p "Enter your login name:" USERNAME			#输入语句，将用户的输入保存到USERNAME变量中
if [ $USERNAME = "RHEL8" ]; then					#对用户名进行判断，如果为真则打印字符串和用户名
		echo "Hello $USERNAME"
fi													#结束符fi非常重要，千万不要忘记

在此例中，[]采用的是test命令的简写格式，如果输入错误的名字，则什么也不显示，对这个例子进行修改，要求如果输入错误的话，就输出“sorry , the name you entered is not correct.”，则需要使用if…else语句，其格式为：
if  [ condition  ]；then 
	command1
	command2
	...
else
	command1
	command2
	...
fi

if…else语句的执行顺序为，当if后的条件为真时，则执行then和else之间的命令，如果条件为假，则执行else与fi之间的命令，所以可能有选择地执行命令，下面就对上述示例进行修改，改动后的脚本内容如下：
#!/bin/bash

read -p "Enter your login name:" USERNAME
if [ $USERNAME = "RHEL8" ]; then
		echo "Hello $USERNAME"
else
		echo "Sorry,the name you entered is not correct."
fi

if…elif…fi语句可以进行多重判断，其使用的语法格式为：
if  [ condition1  ]; then 
	command1
	...
elif [ condition2  ]; then
	command1
	...
elif [ condition  ]; then
	command1
	...
else
	command1
	...
fi	
 
其中elif可以是任意多个，但是一般情况为了程序的清晰度，不推荐使用太多的elif语句，如果分支过多，则可以采用case分支。

case分支
case可实现多分支，用来替换if…elif…fi语句，减少elif的使用，是脚本结构更加清晰，case命令的基本命令格式为：
case  variables in 
var1)
	commands
	...
	;;
var2)						#变量var可以由多个
	commands
	...
	;;
*)
	commands
	;;

esac
	
case命令的执行顺序为：首先用变量值与值1进行对比，如果相同，则执行相应命令，否则与值2进行对比，如果相同执行相应命令，依此类推，如都不匹配，则执行默认的命令，即*)内的命令。需要注意的是，每个段落里最后都要由两个“;;”结尾，以表示命令结束，并且最后应该使用esac来结尾,关于case的最好的例子，都在/etc/init.d/目录，如ssh脚本文件最后一部分就是case命令最好的实例。

10.1.6. 循环结构
循环命令就是反复执行一个操作或者一组命令，直到达到某个条件为止，bash中有三种循环，分别是for循环、while循环和until循环。
◆for循环
for循环能够根据in后面的变量数目执行循环，其命令语法如下：
for  variable in var1 var2 var3
do 
	command
	...
done

for循环第一次执行循环时，会把变量var1的值赋予variable，然后将该变量带入到do和done之间的命令并执行，当命令执行完毕，再将var2的值赋予自定义变量，接着再带入自定义变量并执行do和done之间的命令，一直到in后面的列表中变量值全部赋予完毕后，for循环才结束。

还可以数值范围充当循环变量，格式如下：
for  variable in {init..end}				
do 
	command
	...
done

如果是一个数值范围，变量将从数值的范围获得值，从初识数值开始，之后将该数值带入到do和done之间的命令中，命令执行完成后，初始数值将自动加1，再次由自定义变量传入到do和done之间的命令中，如此循环往复，直到变量值等于终止数值为止，for循环结束。下面通过实例学习for循环的用法，编写一个脚本，此脚本将会扫描局域网络，然后将活动或说已被占用的IP地址打印出来，脚本代码如下：
cat ping.sh
#!/bin/bash						#shebang固定格式

for i in {3..254}; 				#for循环
	do 
		ping -c 1 -w 1 192.168.1.$i &>/dev/null && echo 192.168.1.$i is alive.			#ping命令的-c参数表示ping的次数，参数-w则表示deadline时间为1秒，防止ping不通死等的情况发生，/dev/null是bash中的垃圾桶，&&表示仅当ping通才打印alive字符
	
	done
	
运行此脚本时，每次循环，都会运行一次ping命令，ping局域网中的一个IP地址，如果能ping通，则条件为真，就执行echo命令打印次IP地址 ，如果条件不满足，则继续循环，一直到扫描到局域网地址的上限254为止，也就是将局域网中的IP都ping一遍，打印有响应的IP地址，最后for循环结束，执行结果如下：
192.168.1.103 is alive
192.168.1.111 is alive
192.168.1.115 is alive
192.168.1.116 is alive
192.168.1.123 is alive
192.168.1.171 is alive

除此之外，for循环还常被用做单行命令来使用，实例在下面。

◆while循环
while循环的语法格式为：
while   [ condition ]
do
	command
	...
done 

while循环能够对后面的条件进行判断，当条件为真时，就执行do和done之间的命令，直到条件为假时，退出循环。通过实例学习while循环用法，while脚本内容如下：
cat while.sh
#!/bin/bash

while [ 1 ]									#条件用于为1，即这是个死循环
do
			read -p "Login name:" USERNAME
			if [ $USERNAME = "admin" ]; then
					echo "Hello,$USERNAME"
					break
			fi
			echo "Sorry,the name you entered is not correct."
done
 
此程序实现的功能是始终让用户输入用户命令，直到输入正确的用户名为止，其中将条件始终为1，说明条件始终成立，其实就是一个死循环，然后在里面加入判断，当用户名等于admin时退出循环，使用break命令，这个命令是结束循环的意思，此外，while循环还可以编出只有一行的循环命令，在bash中十分常用，实例如下：
while [ 1 ];do curl http://127.0.0.1;done				#让curl反复访问本机IP,即反复执行一个命令
while true;do curl http://127.0.0.1;done				#等价命令
while /bin/true;do curl http://127.0.0.1;done			#等价命令

快捷键Ctrl+C结束死循环。

◆until循环
until循环和while循环正好相反，是只有当条件为真的时候才退出循环。
until循环的命令格式为：
until  [ condition ]
do
	command1
	……
done

通过实例学习until循环的用法，until.sh脚本内容如下：
cat until.sh
#!/bin/bash

read -p "Login name:" USERNAME

until [ $USERNAME = "admin" ]
do
	echo "Sorry,$USERNAME is not correct."
	read -p "Login name:" USERNAME
	
done

echo "Hello,$USERNAME"
 
上述实例和while循环的实例效果相同，只是采取了不同的循环方式而已。万变不离其宗，Shell script脚本和其他编程语言一样，也是由顺序，分支和循环结构构成，完成相对复杂的功能。

函数和数组
shell script支持函数和数组，使用函数是为了脚本代码更加易读和结构化，推荐大家使用函数实现脚本的模块化，定义和调用一个函数十分简单，下面就以简单的脚本deploy_nginx.sh来演示函数实的基本使用,具体实现如下：
cat deploy_nginx.sh
#!/bin/bash

deploy_nginx()						#定义函数用于部署Nginx
{
dnf install -y nginx
}

deploy_nginx						#调用函数

还可在调用函数间插入如下命令获得函数的执行情况：
echo $?								#测试上一条命令是否执行成功
sleep 10							#停顿10秒，便于查看结果

脚本中尽量使用函数将脚本结构化，这样的脚本既容易读，又容易维护，推荐大家采用，此外函数还支持传参等操作，需要的朋友可以参考相关文档自学。

数组虽说不是很常用，但定义和使用起来却很简单，这是因为bash只支持一维数组，不支持多维数组，且数组元素的下标从0开始编号。获取数组中的元素要通过下标，下标是整数或算术表达式(>=0)，下面就从数组的定义开始说起。

要在bash中定义一个数组，有两种方法，分别是直接定义法和下标定义法：
直接定义法：
array=(a b c) 		#空格分隔
 
下标定义法：
array[0]="a"
array[1]="b"
array[2]="c"

无论哪种方法定义，都可以使用如下方法遍历数组的值：
for VAR in ${array[@]}; do echo $VAR; done				#for循环单行命令实例
a
b
c

或:
echo ${array[*]}
a b c

上述循环中使用@表示下标，自动从0开始计数，而echo命令中的${array[*]}则表示数组中的全部值。

10.1.7.脚本调试
通过前面几节的内容已经能够掌握Shell脚本的编写了，但是对于刚学习Shell脚本的读者朋友来说，脚本出错是避免不了的事情，这就需要能够对脚本进行简单调试和排错。bash命令提供了对脚本调试的一些命令选项，命令的下达方式为：
bash -x	deploy_nginx.sh
+ deploy_nginx
+ dnf install -y nginx
Updating Subscription Management repositories.
Last metadata expiration check: 0:47:05 ago on Sun 13 Oct 2019 07:33:42 PM EDT.
Package nginx-1:1.14.1-9.module+el8.0.0+4108+af250afe.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!

及：
bash -n deploy_nginx.sh

bash命令可以在程序运行前检查语法错误，上述参数中，-x参数可以将脚本的内容在执行时显示出来，方便用户进行跟踪调试错误，而-n参数不执行脚本，只是检查脚本的语法错误。shell script语法十分简单，但要精通却不容易，需要大量的编写脚本才能有所精进，笔者的一些脚本保存在GitHub，欢迎大家来Fork，GitHub地址如下：
https://github.com/HenryHo6688/ShellScripts.git

10.1.8 Shell script开发实践
学完了Shell script开发知识，总感觉这些Shell编程的基础知识很难联系实际应用中，授之以鱼，更要授之以渔，为了帮助大家学以致用和巩固上述Shell编程基础，下面就以第1章中PXE服务器繁琐的部署为例来实现其安装的自动化，全部过程通过Shell Script脚本来实现，更为重要的是，创建这个脚本的全过程可以帮助大家掌握Shell编程的实际方法和思路。

Shell编程可以说是相对较为简单的一种编程开发了，而部署脚本又是Shell编程中比较简单的，最简单的方法便是将成功部署的各个命令，按照部署时的顺序集中到一起，将它们保存为一个Shell脚本文件，下面先来实现这一步骤，需要准备的是将RHEL 8的DVD光盘镜像先下载好并至于执行脚本的目录下。
vi deploy_pxe_rhel8.sh

汇总的部署命令文件，也就是脚本的雏形如下：
hostnamectl set-hostname pxe.example.com							   #配置PXE服务器的主机名和静态解析
vi /etc/hosts

添加如下内容：
192.168.1.168	pxe.example.com											#编辑/etc/hosts文件，新增静态解析

systemctl stop firewalld												#停止并禁用防火墙服务
systemctl disable firewalld
dnf install dhcp-server tftp tftp-server syslinux httpd xinetd wget -y 		#安装DHCP，TFTP和HTTP服务

vi /etc/dhcp/dhcpd.conf													#配置DHCP服务

文件末尾追加如下内容：
subnet 192.168.1.0 netmask 255.255.255.0 {								#定义所分配的网段
 range 192.168.1.201 192.168.1.212;										#定义IP地址池，可分配地址是从201到240
 option routers 192.168.1.1;											#配置默认网关地址
 option domain-name-servers 192.168.1.1;								#配置默认DNS服务器地址
 
 # IP of PXE Server
next-server 192.168.1.168;												#指定PXE服务器的IP地址
filename "pxelinux.0";													#指定PXE引导文件名称
}
										
vi /etc/xinetd.d/tftp													#配置TFTP服务

添加如下内容：
service tftp
{
disable         = no
socket_type     = dgram
protocol        = udp
wait            = yes
user            = root
server          = /usr/sbin/in.tftpd
server_args     = -v -s /var/lib/tftpboot
per_source      = 11
cps             = 100 2
flags           = IPv4
}
									
mkdir /var/lib/tftpboot/pxelinux.cfg																#复制网络引导程序
mkdir /var/lib/tftpboot/networkboot
cp -v /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot
cp -v /usr/share/syslinux/menu.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/memdisk /var/lib/tftpboot
cp -v /usr/share/syslinux/mboot.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/chain.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/ldlinux.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/libutil.c32 /var/lib/tftpboot

mount -o loop rhel-8.0-x86_64-dvd.iso /mnt/															#将RHEL8的ISO安装镜像挂载到/mnt目录下
cd /mnt/
cp -rf * /var/www/html/
rm -rf /etc/httpd/conf.d/welcome.conf
cp /mnt/images/pxeboot/vmlinuz /var/lib/tftpboot/networkboot/
cp /mnt/images/pxeboot/initrd.img /var/lib/tftpboot/networkboot/

vi /var/lib/tftpboot/pxelinux.cfg/default																#配置网络引导菜单，仅作参考，可自行定义

添加如下内容：
default menu.c32
prompt 0
timeout 30
MENU TITLE 	PXE Menu
LABEL rhel8_x64
MENU LABEL RHEL 8_X64
KERNEL /networkboot/vmlinuz
APPEND initrd=/networkboot/initrd.img inst.repo=http://192.168.1.168/ ks=http://192.168.1.168/rhel8.cfg

PXE_ROOT_PASSWD=`openssl passwd -1 -salt "root" "hhhhhhhh"`												#创建root密码的密文
vi /var/www/html/rhel8.cfg																				#创建Kickstart自动安装文件，仅供参考

#platform x86, AMD64, or Intel EM64T
lang en_US
keyboard us
timezone America/New_York --isUtc
rootpw $1$/5SPAsu2$YuBLsq0wFbTgFaOqzykBn/ --iscrypted
reboot
text
url --url=http://192.168.1.168/BaseOS/
bootloader --location=mbr --append="rhgb quiet crashkernel=auto"
zerombr
clearpart --all --initlabel
autopart
auth --passalgo=sha512 --useshadow
selinux --disabled
firewall --disabled
skipx
firstboot --disable
%packages
@standard
@web-server
%end
repo --name=appstream --baseurl=http://192.168.1.168/AppStream/

将所有命令行整理好了之后，全部保存到一个文件，这个步骤很简单，唯一的疑问是，如果将它作为部署脚本，能否达成自动部署PXE服务的功能？事实上，这个脚本是无法执行到最后一个命令，为什么呢？因为执行第二个命令时，vi编辑器就在等待你下达具体的编辑操作，其实不止是第二条命令，下面还有好多vi命令呢，这些都是这个“脚本”的死穴，故要想让脚本中的所有命令从第一条执行到最后一条，也没有想象的那么简单，问题的关键是如何解决上述问题，如果依旧使用vi命令来实现配置文件的修改，那可以肯定的是依旧无解，因为vi就是一个所见即所得的编辑器，要用vi就只能以其设计好的方式编辑和保存文件，解决这个问题只能进行等价替代，那如何实现等价替代呢？主要有以下几个方法可以实现：
1.通过echo命令对文件进行修改
如第二条命令，就完全可以使用echo命令和输出重定向来实现，具体操作如下：
echo "192.168.1.168	pxe.example.com" >> /etc/hosts

2.通过echo命令及EOF文件终止符实现
根据上述的替换法，命令可以执行下去了，不过到了DHCP配置文件哪里，用echo命令实现起来就有点麻烦了，这时就要请出EOF(End Of File)文件终止符的用法了，关键操作如下：
cat > /etc/dhcp/dhcpd.conf <<EOF
subnet 192.168.1.0 netmask 255.255.255.0 {
 range 192.168.1.201 192.168.1.212;	
 option routers 192.168.1.1;
 option domain-name-servers 192.168.1.1;
 
 # IP of PXE Server
next-server 192.168.1.168;
filename "pxelinux.0";	
}
EOF

这样就可将大段配置内容直接追加到配置文件，还可以用于创建TFTP的配置文件：
cat > /etc/xinetd.d/tftp <<EOF												#配置TFTP服务
service tftp
{
disable         = no
socket_type     = dgram
protocol        = udp
wait            = yes
user            = root
server          = /usr/sbin/in.tftpd
server_args     = -v -s /var/lib/tftpboot
per_source      = 11
cps             = 100 2
flags           = IPv4
}
EOF

此外，下面的大段配置文件也可以通过这种方法实现，如rhel8.ks文件等文件。

通过上述几种方法，终于可将命令从头执行到尾了，唯一的问题最后创建rhel8.ks文件时需要将先前生成的密文传入到ks文件中，这也不难，可通过定义一个Shell变量将密文传入到所生成的文件，这样上述脚本就进化为如下这个样子：
hostnamectl set-hostname pxe.example.com
echo "192.168.1.168	pxe.example.com" >> /etc/hosts
systemctl stop firewalld
systemctl disable firewalld
dnf install dhcp tftp tftp-server syslinux httpd xinetd wget -y
cat > /etc/dhcp/dhcpd.conf << EOF
subnet 192.168.1.0 netmask 255.255.255.0 {
 range 192.168.1.201 192.168.1.212;	
 option routers 192.168.1.1;
 option domain-name-servers 192.168.1.1;
 
 # IP of PXE Server
next-server 192.168.1.168;
filename "pxelinux.0";	
}
EOF
										
cat > /etc/xinetd.d/tftp <<EOF
service tftp
{
disable         = no
socket_type     = dgram
protocol        = udp
wait            = yes
user            = root
server          = /usr/sbin/in.tftpd
server_args     = -v -s /var/lib/tftpboot
per_source      = 11
cps             = 100 2
flags           = IPv4
}
EOF

mkdir /var/lib/tftpboot/pxelinux.cfg									#复制网络引导程序
mkdir /var/lib/tftpboot/networkboot
cp -v /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot
cp -v /usr/share/syslinux/menu.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/memdisk /var/lib/tftpboot
cp -v /usr/share/syslinux/mboot.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/chain.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/ldlinux.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/libutil.c32 /var/lib/tftpboot

mount -o loop rhel-8.0-x86_64-dvd.iso /mnt/
cd /mnt/
cp -rf * /var/www/html/
rm -rf /etc/httpd/conf.d/welcome.conf
cp /mnt/images/pxeboot/vmlinuz /var/lib/tftpboot/networkboot/
cp /mnt/images/pxeboot/initrd.img /var/lib/tftpboot/networkboot/

cat > /var/lib/tftpboot/pxelinux.cfg/default << EOF
default menu.c32
prompt 0
timeout 30
MENU TITLE 	PXE Menu
LABEL rhel8_x64
MENU LABEL RHEL 8_X64
KERNEL /networkboot/vmlinuz
APPEND initrd=/networkboot/initrd.img inst.repo=http://192.168.1.168/ ks=http://192.168.1.168/rhel8.cfg
EOF

PXE_ROOT_PASSWD=`openssl passwd -1 -salt "root" "hhhhhhhh"`
cat > /var/www/html/rhel8.cfg << EOF
#platform x86, AMD64, or Intel EM64T
lang en_US
keyboard us
timezone America/New_York --isUtc
rootpw $1$/5SPAsu2$YuBLsq0wFbTgFaOqzykBn/ --iscrypted
reboot
text
url --url=http://192.168.1.168/BaseOS/
bootloader --location=mbr --append="rhgb quiet crashkernel=auto"
zerombr
clearpart --all --initlabel
autopart
auth --passalgo=sha512 --useshadow
selinux --disabled
firewall --disabled
skipx
firstboot --disable
%packages
@standard
@web-server
%end
repo --name=appstream --baseurl=http://192.168.1.168/AppStream/
EOF

这样PXE服务器自动安装的脚本就初具雏形了，可以尝试运行，具体操作如下：
chmod +x vi deploy_pxe_rhel8.sh
deploy_pxe_rhel8.sh | tee debug.log							#可使用tee命令将脚本的输出2份，一份为屏幕，一份为文件

可以通过运行所产生的debug.log来对脚本进行调试，调试通过后再返回到代码，这个脚本看上去有点凌乱，虽然只是开发一个简单的Shell脚本，也不应该不把Shell编程不当成编程，同样应该遵循一定开发的基本规则，如模块化规则，优化代码等，模块化可以令脚本的逻辑更加清晰，后续的可维护性更强，那如何实现脚本的模块化呢？学以致用，就使用前面所学的Shell函数来实现，至于优化，由于这个脚本比较简单，故可优化的地方不多，废话不多说，直接敲代码，开发和优化后最终的脚本代码如下：
cat deploy_pxe_rhel8.sh
#!/bin/bash
################################################################################
#Purpose:Deploy and configure PXE Server
#Author(Email):Henry Ho(hxl2000@gmail.com)
#Environment:RHEL 8 server with GUI
################################################################################
PXE_IP=192.168.1.168

stop_firewalld(){
systemctl stop firewalld
systemctl disable firewalld
hostnamectl set-hostname pxe.example.com
echo "$PXE_IP	pxe.example.com" >> /etc/hosts
}

deploy_pxe_server(){
dnf install dhcp-server tftp tftp-server syslinux httpd xinetd -y
}

cfg_dhcpd(){
cat << EOF > /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
ddns-update-style interim;
ignore client-updates;
authoritative;
allow booting;
allow bootp;
allow unknown-clients;

# internal subnet for my DHCP Server
subnet 192.168.1.0 netmask 255.255.255.0 {
range 192.168.1.200 192.168.1.212;
option domain-name-servers 192.168.1.1;
option domain-name "pxe.example.com";
option routers 192.168.1.1;
option broadcast-address 192.168.1.255;
default-lease-time 600;
max-lease-time 7200;

# IP of PXE Server
next-server $PXE_IP;
filename "pxelinux.0";
}
EOF
}

cfg_tftpd(){
cat << EOF > /etc/xinetd.d/tftp
service tftp
{
 socket_type = dgram
 protocol    = udp
 wait        = yes
 user        = root
 server      = /usr/sbin/in.tftpd
 server_args = -s /var/lib/tftpboot
 disable     = no
 per_source  = 11
 cps         = 100 2
 flags       = IPv4
}
EOF

cp -v /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot
cp -v /usr/share/syslinux/menu.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/memdisk /var/lib/tftpboot
cp -v /usr/share/syslinux/mboot.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/chain.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/ldlinux.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/libutil.c32 /var/lib/tftpboot
mkdir /var/lib/tftpboot/pxelinux.cfg
mkdir /var/lib/tftpboot/networkboot
}

copy_setup_file(){
cd
mount -o loop rhel-8.0-x86_64-dvd.iso /mnt																	#挂载RHEL 8的DVD镜像到/mnt目录

或：
mount /dev/cdrom /mnt																						#或直接挂载光盘到/mnt目录
cd /mnt/
cp -rf * /var/www/html/
cp /mnt/images/pxeboot/vmlinuz /var/lib/tftpboot/networkboot/
cp /mnt/images/pxeboot/initrd.img /var/lib/tftpboot/networkboot/
cd
umount /mnt/
}

cfg_httpd(){
rm -rf /etc/httpd/conf.d/welcome.conf
systemctl start httpd
systemctl enable httpd
}

create_kickstart_menu(){
PXE_ROOT_PASSWD=`openssl passwd -1 -salt "root" "hhhhhhhh"`

cat << EOF > /var/www/html/rhel8.cfg
#platform=x86, AMD64, or Intel EM64T
lang en_US
keyboard us
timezone America/New_York --isUtc
rootpw $PXE_ROOT_PASSWD --iscrypted
reboot
text
url --url=http://$PXE_IP/BaseOS/
bootloader --location=mbr --append="rhgb quiet crashkernel=auto"
zerombr
clearpart --all --initlabel
autopart
auth --passalgo=sha512 --useshadow
selinux --disabled
firewall --disabled
skipx
firstboot --disable
%packages
@standard
@web-server
%end
repo --name=appstream --baseurl=http://$PXE_IP/AppStream/
EOF

cat << EOF > /var/lib/tftpboot/pxelinux.cfg/default
default menu.c32
prompt 0
timeout 30
MENU TITLE 	PXE Menu
LABEL rhel8_x64
MENU LABEL RHEL 8_X64
KERNEL /networkboot/vmlinuz
APPEND initrd=/networkboot/initrd.img inst.repo=http://$PXE_IP/ ks=http://$PXE_IP/rhel8.cfg
EOF
}

restart_services(){
systemctl start xinetd
systemctl enable xinetd
systemctl start dhcpd.service
systemctl enable dhcpd.service
}

stop_firewalld
deploy_pxe_server
cfg_dhcpd
cfg_tftpd
copy_setup_file
cfg_httpd
create_kickstart_menu
restart_services

这个脚本涉及前面所学的Shell开发知识，并结合部署PXE服务的实际应用，学以致用地实现了PXE服务器的自动部署脚本，当然，这个脚本还有很多地方能够优化，建议大家熟练掌握后再自行优化，有了这个脚本，部署PXE服务器就不再是一件麻烦事了,其实，比脚本代码本身更为重要的是开发Shell脚本的思路和方法。此外由于Shell脚本的执行效率及难度，所以即使会用Python等高级语言，解决问题建议还是首先考虑通过Shell Script解决，因为最为高效和简单。

最后，提醒虚拟机安装测试的朋友需要注意两点，一是一定要注意网络类型是否一致，网络类型要么全是Bridge，要么全是NAT，因为PXE服务器采用Bridge及固定IP地址，而创建新虚拟机默认是NAT网络，其次，作为使用PXE服务进行安装的虚拟机，内存要大于2GB，否则安装过程中将会报错。

10.2. Python 3开发初阶
Python是除Shell script之外，在系统管理方面，使用最多的语言之一，如著名的Ansible，Cobbler，Fabric及SaltStack等自动化工具都是由Python开发的。Python是Guido van Rossum于1989年创建的一门高级编程语言，可以从权威的TIOBE编程语言排行榜来观察Python的趋势，最新的TIOBE Index for March 2019地址如下：
https://www.tiobe.com/tiobe-index/

从其统计结果来看，Python长期稳居第三，仅排在C和Java之后，Python之所以流行，主要是因为它高雅(Elegant)的代码风格及超完善的基础库，框架和大量第三方库等，涵盖了Web，网络，图形界面(GUI),数据库,文件和文本等方方面面，这样用Python开发起来就十分便捷和高效了，许多著名公司和机构都在使用Python，如Google，Facebook，NASA（美国航空航天局）等，Python的Logo如图10-1所示。

图10-1 Python的Logo(图片来源：Python官方首页)

Python的官方文档地址如下：
https://www.python.org/doc/						#分为2.x和3.x两大分支，阅读官方文档要注意版本

Python的官方中文文档地址如下：
◆Python 3.7
https://docs.python.org/zh-cn/3.7/tutorial/index.html

◆Python 2.7
https://docs.python.org/zh-cn/2.7/tutorial/index.html

本章主要是使用Python来弥补shell script所不能完成的功能，由于Python需要解释执行，故其效率没有Shell script高，但优点是可以调用完善的基础库和模块，第三方库和模块，实现一些较为复杂的功能，下面照例先来一个Python版的Hello world，具体实现方法如下：
vi helloworld.py								#Python的源代码程序使用py作为扩展名
print ('Hello world!')

保存退出后，在命令行运行如下命令：
python3 helloworld.py
Hello world!

如果没有安装Python，可运行如下命令安装：
dnf install -y python36						#安装默认的Python 3.6版本

成功安装后，可用如下命令查看Python版本：
python3.6 --version
Python 3.6.8

需要提醒大家的是，目前Python有经典的2.x版本，和3.x版本两大分支，简而言之，二者语法略有差异，2.x版本的官方支持2020年，即将退休，故RHEL 8默认的版本为3.6.8，下面就以RHEL 8默认的Python 3.6.8版本为例来学习。

照例还是先从变量说起，由于bash shell比较简单，故数据类似也比较简单，高频使用的有数值和字符串类型，不过本质上bash只有一种数据类型，那就是字符串，数值可视为特殊字符串，但Python毕竟是一种完善的高级脚本语言，故Python的数据类型比Shell丰富许多，高频使用的有如下几种：
◆整数，如-7，1，8，90等；
◆浮点数，如3.1416,-6.18,还可以使用科学计数法，如3.14e6等价于3140000；
◆字符串，如happy,I\'m happy等，'或"需要使用\转义字符来标识；
◆布尔值，如true和false。

此外，Python还支持复杂的数据类型，如列表，元组，字典和集合等，
◆列表：有序集合的可变的序列，列表中的元素可添加或删除；
◆字典：可定义键和值之间一对一的关系；
◆元组：和列表很类似，但其是不可变的序列；
◆集合：

10.2.1.输入和输出
Shell script中使用read和echo作为输入和输出语句，而在Python中，则对应input()，raw_input()和print()函数了，类似C语言的输入scanf()和输出函数printf()，前面已经说过shell script其实只有一种字符串数据类型，而Python则支持多种数据类型，所以有两个输入函数，input()函数负责数值输入，而另外一个则是负责字符串的输入，如需提示字符串，只需在input()或raw_input()函数中添加即可，十分方便，具体方法如下：
python3.6
>>> rhel = input()
8.0

然后输入8.0,在使用打印函数即可打印：
>>> print(rhel)
8.0

之后输入字符串，具体操作如下：
>>> r8 = input()
RHEL 8

再使用print函数进行打印，结果如下：
>>> print(c8)
RHEL 8

如果要在用户输入数值前出现提示字符串，可以使用如下格式：
>>> ver = input("Enter RHEL version：")
Enter RHEL version：8.0

这次就有了提示字符串了，在此打印验证：
>>> print(ver)
8.0

如果要在用户输入字符串前出现提示字符串，可以使用如下格式：
>>> name = input("Enter distro. name:")
Enter distro. name:RHEL 8

照例打印验证：
>>> print(name)
RHEL 8

如果要打印的字符串之前也出现类似的提示字符串的话，只需在print后添加即可，具体操作如下：
print("Linux distro. is:",name)
Linux distro. is: RHEL 8

这次所打印的内容就出现了提示了。

还可以打印更为复杂的，九九乘法表和心形图案的范例如下：
>>> print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))
1*1=1
1*2=2  2*2=4
1*3=3  2*3=6  3*3=9
1*4=4  2*4=8  3*4=12 4*4=16
1*5=5  2*5=10 3*5=15 4*5=20 5*5=25
1*6=6  2*6=12 3*6=18 4*6=24 5*6=30 6*6=36
1*7=7  2*7=14 3*7=21 4*7=28 5*7=35 6*7=42 7*7=49
1*8=8  2*8=16 3*8=24 4*8=32 5*8=40 6*8=48 7*8=56 8*8=64
1*9=9  2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81

不仅可以打印数字表达式，还可以打印图案：
>>> print('\n'.join([''.join([('IloveU'[(x-y)%len('IloveU')]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))

                eUIloveUI           IloveUIlo
            loveUIloveUIloveU   veUIloveUIloveUIl
          IloveUIloveUIloveUIloveUIloveUIloveUIlove
         IloveUIloveUIloveUIloveUIloveUIloveUIloveUI
        IloveUIloveUIloveUIloveUIloveUIloveUIloveUIlo
        loveUIloveUIloveUIloveUIloveUIloveUIloveUIlov
        oveUIloveUIloveUIloveUIloveUIloveUIloveUIlove
        veUIloveUIloveUIloveUIloveUIloveUIloveUIloveU
        eUIloveUIloveUIloveUIloveUIloveUIloveUIloveUI
        UIloveUIloveUIloveUIloveUIloveUIloveUIloveUIl
         loveUIloveUIloveUIloveUIloveUIloveUIloveUIl
          veUIloveUIloveUIloveUIloveUIloveUIloveUIl
          eUIloveUIloveUIloveUIloveUIloveUIloveUIlo
            loveUIloveUIloveUIloveUIloveUIloveUIl
             veUIloveUIloveUIloveUIloveUIloveUIl
              UIloveUIloveUIloveUIloveUIloveUIl
                oveUIloveUIloveUIloveUIloveUI
                  UIloveUIloveUIloveUIloveU
                    oveUIloveUIloveUIlove
                       IloveUIloveUIlo
                          eUIloveUI
                             ove
                              e

此外，需要特别注意的是，Shell script中默认编码为Unicode，对于Python，就稍微复杂一些了，Python2.x中默认编码为ASCII，而Python3中默认编码为Unicode，Unicode可直接多语言支持，所以在Python代码的注释中注明代码的编码十分重要，具体方式如下：
#coding=utf-8							

10.2.3.逻辑结构
Shell script都支持三大逻辑结构，Python是一种高级语言，所以支持更为完善的流程结构，如顺序机构，分支结构和循环结构，顺序结构最为简单，只需将语句依次列出即可，下面就以大小写字母转换为例来演示顺序结构。

大小写字母转换的算法十分简单，由于大小写字母均为ASCII码，即无论大小写，一个字母对应一个ASCII数值，且小写字母的十进制值较相应的大写字母大32，大写变小写只需加上32即可实现，麻烦的是如何获得一个字母的ASCII码的十进制值和将一个十进制的ASCII码打印为字母，这就需要请出两个Python函数了，ord()和chr()，它们可以实现，下面就来编码，代码如下：
cat cu2l.py
#!/usr/bin/python3.6												#shebang指定Python解释器路径
u = input("Enter an uppercase letter:")								#获得用户所输入的大写字母
du=ord(u)															#将用户输入的字母转换为10进制数
print ("The lower case letter you entered is:",chr(du + 32))			#加32打印

更进一步，还可以实现字符串的大小写转换，只需使用现成的函数str.lower()和str.upper()即可实现，大写变小写代码如下：
cat u2l.py
#!/usr/bin/python3.6
su = 'RHEL 8' 			#为变量su赋值纯大写字符串
print(str.lower(su))				#打印为小写字符串

执行上述代码，结果如下：
chmod +x u2l.py
./u2l.py
rhel 8

小写变大写代码如下：
cat l2u.py
#!/usr/bin/python3.6
sl = 'rhel 8' 					#为变量su赋值纯小写字符串
print(str.upper(sl))				#打印为大写字符串

执行上述代码，结果如下：
chmod +x l2u.py
./12u.py
RHEL 8

上述这些代码都是顺序结构的Python小程序，顺序结构十分简单，此处就不在赘述了。

分支结构
Python的分支结构和shell script十分类似，下面依然以shell script中的login程序为例来演示Python的分支结构，if语句的完整形式就是：
if condition1:
    branch1
elif condition2:
    branch2
elif condition3:
    branch3
else:
    brahch4
	
每个branch至少有一条Python语句，if语句是从上往下执行，如果某个条件为True，则执行该条件所对应的语句，忽略掉下面的elif和else，从最简单的if分支结构开始，来学习Python的if语句，再以shell script的login登录判断为例，用Python来实现，代码如下：
cat login.py
#!/usr/bin/python3.6									#shebang固定格式，指定脚本的解释器

username = input("Enter your login name:")				#输入语句，将用户所输入的字符串保存到username变量中
if username == 'rhel' :								#对用户名进行判断，如果为真则打印字符串和用户名
        print ("Hello", username)

如果输入rhel则会打印Hello rhel字符串，结果如下：
chmod +x login.py
./login.py
Enter your login name:rhel
Hello rhel

对上述代码进行扩展，添加else分支，代码如下：
#!/usr/bin/python3.6

username = input("Enter your login name:")
if username == "rhel" :							#对用户名进行判断，如果为真则打印字符串和用户名,为假则打印Sorry,the name you entered is not correct
                print ("Hello", username)
else:
                print ("Sorry,the name you entered is not correct.")

再来一个通过数值判断的例子，输入一个图书销量，根据不同的数量打印不同的评估结果，代码如下：
#!/usr/bin/python3.6
quantity = int(input("Enter the amount:"))		#用户输入的数量保存到变量quantity，并进行数据类型转换
if quantity >= 100:								#销量大于等于100，评价为cool
    print('quantitytity is ', quantity)			
    print('cool')

elif quantity >= 50:							#销量大于等于50，评价为good
    print('quantitytity is ', quantity)
    print('good')

else:
    print('quantitytity is ', quantity)			#销量小于50，评价为Average
    print('Average')

上述代码将根据if语句判断来执行不同的分支，进行不同操作，需要注意的是efif后面没有冒号。

循环结构
循环结构主要的用途就是数学计算，尤其是需要大量重复运算的，如著名数学家高斯童年所遇到的问题，需计算1+2+3+...+100，当年高斯已经给出了经典的算法，套用即可，Python代码如下：
python3.6
Python 3.6.8 (default, May 21 2019, 23:51:36)
[GCC 8.2.1 20180905 (Red Hat 8.2.1-3)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> (1 + 100) * 50
5050

由于采用了高斯的经典算法，故绕开了繁琐的计算，将问题简化成了加法和乘法，如果采用笨办法来计算，即累加到100，那该计算机中该如何实现呢？先来看一下笨办法的算法，1+2=3，3+3=6，6+4=10，...依此类推，抽象为算法其实就是一个加法等式，只是加数是一个变量，保存累加结果，而被加数则是递增的数值，每次相加的结果都保存到累加变量中即可，要在计算机上实现，通过循环结构来实现最为简单,需要一个累加变量sum和一个循环变量i，sum用于保存前一次相加的结果，充当加数，而i则是循环变量，每次加1，充当被加数，如此待循环变量为100，累加变量的结果就是需要的结果了，Python代码实现如下：
cat for.py
#!/usr/bin/python3.6			#shebang是脚本必不可少的
sum = 0							#初始化sum累加变量，sum的初始化值为0
for i in range(101):			#通过range函数生成一个整数序列
    sum = sum + i
	#sum保存上一次累加变量sum和循环变量i的和，需要注意的是循环体中的语句缩进(四个Tab键)，对Python而言，循环体中的语句如不缩进，就不属于for循环的范围，还会报错
print ("1+2+3+...+100=",sum)	#打印提示字符串和最终的累加结果

需要特别说明的是，for循环中的range()函数，该函数可以自动生成一个整数序列，range(101)便可生成0-100的整数序列，相当于for i in [1,2,3,...,100]，实际运行结果如下：
python3.6 for.py
1+2+3+...+100= 5050

高斯的同学都是这么算的，而当年高斯同学将问题转化为乘法，轻易算出最终结果5050。此外，和Shell script类似，还有一种循环，那就是while循环，判断条件满足，就不断循环，而当条件不满足时退出循环，Pyton实现如下：
cat while.py
#!/usr/bin/python3.6
sum = 0							#初始化sum累加变量，sum的初始化值为0
i = 1							#循环变量初始值为1
while i < 101:
    sum = sum + i				#千万不要忘记缩进(四个空格键)
    i = i + 1					#循环变量每次加1
print ("1+2+3+...+100=",sum)

在循环内部变量n不断自加，直到100时，不再满足while条件，循环退出，运行如上代码，结果如下：
python3.6 while.py
1+2+3+...+100= 5050

此外，Python还提供了break语句和continue语句，break语句用于提前结束循环，而continue语句，则可跳过当前的这次循环，开始下一次的循环,由于很少使用，故此处就不赘述了。

除了数学计算之外，循环还可以可以用于遍历，下面就以最简单的列表(list)为例来演示，当然遍历对象不仅限于列表(list)和元组(tuple)：
cat linux.py
#!/usr/bin/python3.6
Linux_Distro = ['Ubuntu', 'RHEL', 'CentOS','SUSE']
for pop in Linux_Distro:
    print(pop)
	
执行上述代码，会依次打印Linux_Distro的每一个元素：
python3.6 linux.py
Ubuntu
RHEL
CentOS
SUSE

10.2.4. 函数
函数对于编程语言来说，极为重要，前面已经使用了很多Python的基础函数了，如input(),print(),ord(),chr()和rang()这些函数，它们是Python本身提供的，故又称之为基础函数，对于基础函数，拿来主义就可以了，根据其格式直接使用即可，没有太多可说，故此处主要学习如何自定义一个函数，Python中定义一个函数要使用def语句，依次写出函数名，括号和冒号，之后便是所定义的函数体，最后用return语句返回函数值(return的值可有可无，如无则返回none)。

下面就自定义一个十分简单的函数，代码如下：
cat helloworld.py
#!/usr/bin/python3.6
#coding=utf-8					#活学活用，添加默认编码的注释

def helloworld():
	print ("Hello world!")

这样就自定义了一个函数，保存为py文件后，还需要导入，Python的解释程序才能使用此函数，关键操作如下：
python3.6											#进入Python shell
>>> from helloworld import helloworld			#from后为py文件名，import后为自定义函数名

随后直接调用helloworld函数即可，具体操作如下：
>>> helloworld()
Hello world!

上述实现的函数极为简单，仅是打印Hello world!字符串而已，无需向函数传递任何参数，下面就来实现一个需要传递参数的打印函数，代码如下：
cat get_detail.py
#!/usr/bin/python3.6
#coding=utf-8

def get_detail(name,ver):
	print ("Linux distrobution :",name)
	print ("Version:",ver)
	
保存为py文件后，再次导入，具体操作如下：
python3.6										#进入Python shell
>>> from get_detail import get_detail			#from后为py文件名，import后为自定义函数名

随后直接调用helloworld函数即可，具体操作如下：
>>> get_detail("RHEL",8.0)
Linux distrobution : RHEL
Version: 8.0

尽管功能依旧简单，但这个函数已经实现了参数的传递。需要注意的是，定义函数时，需要首先将参数的名字和参数确定下来，这样函数接口就定义好了。以后只需根据定义调用该函数就可以实现相应的功能了。

10.2.5. 模块
所谓模块，本质上就是定义了一些变量，函数和类等内容的一个.py，使用模块的最大优点便是代码重用和高可维护性，还可以避免命名冲突(如变量名称或函数名称等)，此处主要侧重于模块的使用。

由于模块中有大量的变量即功能强大的函数，故常常需要导入某个模块，下面就以系统管理者常用的sys模块为例，使用sys模块之前，首先需要导入该模块，具体方法如下：
import sys

成功导入sys模块后，就可以使用sys模块预置的变量及函数了，下面就以获得路径为例来演示调用sys和os模块中的变量，代码如下：
cat path.py
#!/usr/bin/python3.6
#coding=utf-8

import sys						#导入sys模块
import os						#导入os模块

print(sys.path)					#返回模块的搜索路径
print(sys.platform)				#返回操作系统名称
print(sys.version)				#获取Python的版本信息
print(os.getcwd()) 				#取得当前工作目录

随后运行如下命令：
chmod +x ./path.py
./path.py
['/root', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', '/usr/lib64/python3.6/site-packages', '/usr/lib/python3.6/site-packages']
linux
3.6.8 (default, May 21 2019, 23:51:36)
[GCC 8.2.1 20180905 (Red Hat 8.2.1-3)]
/root

返回的三行信息分别是模块的搜索路径，操作系统名称,Python的版本信息和当前工作目录信息。

和Shell script比较，Python的很多地方甚至更为简单，不过由于Python用途丰富，版本众多，本文内容显然是远远不够的，建议结合工作实际，确定学习方向，还需要多看，多练和多用，和Shell Script一样，笔者的Python实用程序同样分享给大家，欢迎Fork，GitHub地址如下：
https://github.com/HenryHo6688/Python

10.3. 本章小结
至此，Shell script和Python的内容全部学习完毕，掌握到这里，对Shell编程及Python开发也算入了门，每种语言都立足于应用且循序渐进地逐步推进，从变量，输入和输出，程序的逻辑结构再到函数，数组(shell script),模块(Python)等，这些是所有编程语言中最为实用的东西，尤其应该重点掌握Shell Script，不仅仅是语法，更应该从本章的Shell开发实例中掌握Shell编程的思路和方法。尽管所涉及的内容及实例都偏简单，但这正是初学者所需要的，本文的价值就在抛砖引玉，将大家的学习兴趣培养起来，进而自动自发地学习，没有涉及到的内容大家可以自己去扩展和深入。


