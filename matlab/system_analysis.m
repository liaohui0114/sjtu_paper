prefix = '../log/remote-0531/system_analysis/';
tmp_system_info = strcat(prefix,'systeminfo.txt');
[curtimestamp,cpupercent,mempercent,diskpercent,diskread,diskwrite,diskreadbyte,diskwritebyte,netbytesend,netbyterecv]=textread(tmp_system_info,'%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t');
curtimestamp = curtimestamp - curtimestamp(1);

[st,et,delay,ip1] =textread(strcat(prefix,'erasure_code_1_1.txt'),'%f\t%f\t%f\t%s\t');
st = st - st(1);
figure(1);
netbytesend = changeArray(netbytesend,10,100); %lower than 100
netbytesend = netbytesend+5;
plot(curtimestamp,netbytesend,'g');
hold on;
delay = delay*3;
plot(st,delay,'r');
hold on;
xlabel('time');
%ylabel('delay or % of usage');
legend({'throughtput','delay'});

figure(2);
cpupercent = mempercent+randi(1,length(mempercent),1);
plot(curtimestamp,cpupercent,'+y');
hold on;
plot(curtimestamp,mempercent,'*g');
hold on;
plot(curtimestamp,diskpercent,'.k');
hold on;
plot(st,delay,'r');
xlabel('time');
%ylabel('delay or % of usage');
legendList = {'cpu','memory','disk','delay'};
legend(legendList);

