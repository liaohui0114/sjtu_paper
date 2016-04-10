% reference
% r  Red
% g  Green
% b   Blue
% c   Cyan
% m  Magenta
% y  Yellow
% k   Black
% w  White
% 
% 
% +  Plus sign
% o  Circle
% *  Asterisk
% .  Point 
% x    Cross
% 'square' or s    Square 
% 'diamond' or d    Diamond
% ^  Upward-pointing triangle
% v   Downward-pointing triangle
% >  Right-pointing triangle
% 'pentagram' or p    Five-pointed star (pentagram)
% 'hexagram' or h     Six-pointed star (hexagram)


%description:to get system information

serverAddr = {'192.168.3.6','192.168.3.7'};
%serverAddr = {'192.168.3.6'};
%serverAddr = {'192.168.3.7'};
%serverAddr(3) = cellstr('123')
%serverAddr{3} = 'liaohui';

for i=1:length(serverAddr);
    logsByAddr(i).addr = serverAddr{i};
    logsByAddr(i).timestamp = [];
    logsByAddr(i).intervalTime = [];
end;

fid = fopen('../logs-everyday/20160409/agent/log/downloadinfo-6.deb.txt');

while ~feof(fid);
    tmpInfoStr = fgetl(fid);
    [start_time,end_time,intervalTime,filename,filesize,server_ip]=strread(tmpInfoStr,'%f%f%f%s%f%s');
    for i=1:length(serverAddr);
        if strcmp(logsByAddr(i).addr,server_ip);
            
            logsByAddr(i).filename = filename;
            logsByAddr(i).filesize = filesize;
            logsByAddr(i).timestamp = [logsByAddr(i).timestamp,start_time];
            logsByAddr(i).intervalTime = [logsByAddr(i).intervalTime, intervalTime];
            
        end;
    end;
end

[curtimestamp,cpupercent,mempercent,diskpercent,diskread,diskwrite,diskreadbyte,diskwritebyte,netbytesend,netbyterecv] = textread('../logs-everyday/20160409/storage2/log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);


legendList = {};

diskreadbyte = changeArray(diskreadbyte,10,100)

% plot(curtimestamp,diskreadbyte,'r');
% hold on;
% legendList = [legendList,'diskread-bytes'];

diskread = changeArray(diskread,10,100);
plot(curtimestamp,diskread,'k');
hold on;
legendList = [legendList,'diskread-count'];

netbytesend = changeArray(netbytesend,10,100);
plot(curtimestamp,netbytesend,'g');
hold on;
legendList = [legendList,'netsend-bytes'];

netbyterecv = changeArray(netbyterecv,10,10);
plot(curtimestamp,netbyterecv,'m');
hold on;
legendList = [legendList,'netrecv-bytes'];

% cpupercent = changeArray(cpupercent,10,10);
% plot(curtimestamp,cpupercent,'r');
% hold on;
% legendList = [legendList,'cpu-percent'];
% 
% plot(curtimestamp,mempercent,'g+');
% hold on;
% legendList = [legendList,'memory-percent'];
% 
% plot(curtimestamp,diskpercent,'k*');
% hold on;
% legendList = [legendList, 'disk-percent'];

figure(1);
%graph 1
for i=1:length(logsByAddr);
    plot(logsByAddr(i).timestamp,logsByAddr(i).intervalTime);
    hold on;
    
    legendList = [legendList,strcat('delay:',logsByAddr(i).addr)];
end;
grid on;
legend(legendList(1:length(legendList)));
xlabel('timestamp');
ylabel('delay or % of usage');

%graph 2
figure(2);
%%%%
[curtimestamp1,cpupercent1,mempercent1,diskpercent1,diskread1,diskwrite1,diskreadbyte1,diskwritebyte1,netbytesend1,netbyterecv1] = textread('../logs-everyday/20160409/storage1/log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);
[curtimestamp2,cpupercent2,mempercent2,diskpercent2,diskread2,diskwrite2,diskreadbyte2,diskwritebyte2,netbytesend2,netbyterecv2] = textread('../logs-everyday/20160409/storage2/log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);


netsendsum1 = sum(netbytesend1)/(curtimestamp1(end)-curtimestamp1(1))
diskreadsum1 = sum(diskread1)
intervalsum1 = sum(logsByAddr(1).intervalTime)
len1 = length(logsByAddr(1).intervalTime)

netsendsum2 = sum(netbytesend2)/(curtimestamp2(end)-curtimestamp2(1))
diskreadsum2 = sum(diskread2)
intervalsum2 = sum(logsByAddr(2).intervalTime)
len2 = length(logsByAddr(2).intervalTime)



bar([netsendsum1/1000,diskreadsum1,intervalsum1;netsendsum2/1000,diskreadsum2,intervalsum2])
legend('disk-read-total','interval-time-total');
set(gca,'XTickLabel',{'storage1','storage2'});
xlabel('storage1 storage2');
grid on;