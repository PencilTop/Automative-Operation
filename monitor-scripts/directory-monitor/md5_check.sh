#!/bin/bash
# 定义MD5文件保存的路径
#存放MD5校验码的文件位置
md5_path=./md5.sum
#存放校验结果日志文件的位置
md5_log=./md5.log
#监控目录
path=/Users/hugh/monitor
 
# 判断MD5基准校验文件是否存在，不存在则创建此文件,并修改权限只有root用户或者指定用户有读写权限
[ ! -f $md5_path ] && touch $md5_path && chmod 600 $md5_path
#read -p "请输入你需要MD5检验文件的目录,必须以\"/\"开始: " path
if ! echo $path | grep -q "^/";then echo "不是以\"/\"开始";exit 1;fi
 
echo "#################################################"
# 如果所给需要md5校验的目录不存在，或者目录存在但目录下没有一个文件，则返回错误并提示用户
if [ ! -d $path ] || [ `find $path -type f | wc -l` -eq 0 ];then
	echo "错误：路径不存在或者该路径下没有文件"
	exit 1
fi
# 判断基准文件数量
for i in `cat ${md5_path} | awk '{print $2}'`;do 
	[ ! -f $i ] && echo -e "[检测时间：`date +"%Y-%m-%d %T.%N"`]  [文件：$i] \033[31m[MD5结果：去除]\033[0m" 2>&1 | tee -a ${md5_log}
done 
  
for list in `find $path -type f`;do
	echo " list = $list"
	new_md5_arg1=`md5sum $list | awk '{print $1}'`
	new_md5_arg2=`md5sum $list | awk '{print $2}'`
	old_md5_arg2=`awk -v List="$list" '$2 == List{print $2}' $md5_path`
	if [[ "$new_md5_arg2" == "$old_md5_arg2" ]];then
		old_md5_arg1=`awk -v List="$list" '$2 == List{print $1}' $md5_path`
		if [[ ! "$new_md5_arg1" == "$old_md5_arg1" ]];then
			echo -e "[检测时间：`date +"%Y-%m-%d %T.%N"`]  [文件：$list] \033[31m[MD5结果：改变]\033[0m" 2>&1 | tee -a ${md5_log}
		else
			echo -e "[检测时间：`date +"%Y-%m-%d %T.%N"`]  [文件：$list] \033[32m[MD5结果：未改变]\033[0m" 
		fi
	else
		md5sum $list >> $md5_path
		echo -e "[检测时间：`date +"%Y-%m-%d %T.%N"`]  [文件：$list] \033[31m[MD5结果：添加]\033[0m" 2>&1 | tee -a ${md5_log}
	fi
	# 如果文件数量大，可以把sleep的时间间隔设置小点。
	sleep 1
done     
