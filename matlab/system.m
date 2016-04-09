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

serverAddr = {'127.0.0.1','192.168.1.1'};
%serverAddr(3) = cellstr('123')
%serverAddr{3} = 'liaohui';

for i=1:length(serverAddr);
    logsByAddr(i).addr = serverAddr{i};
    logsByAddr(i).timestamp = [];
    logsByAddr(i).intervalTime = [];
end;

fid = fopen('../log/downloadinfo-10.mkv.txt');

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

[curtimestamp,cpupercent,mempercent,diskpercent,diskread,diskwrite,diskreadbyte,diskwritebyte,netbytesend,netbyterecv] = textread('../log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);


legendList = {};

% diskreadbyte = changeArray(diskreadbyte,10,100)
% 
% plot(curtimestamp,diskreadbyte,'r');
% hold on;
% legendList = [legendList,'diskread-bytes'];
% 
% diskread = changeArray(diskread,10,100);
% plot(curtimestamp,diskread,'k');
% hold on;
% legendList = [legendList,'diskread-count'];

% netbytesend = changeArray(netbytesend,10,100);
% plot(curtimestamp,netbytesend,'g');
% hold on;
% legendList = [legendList,'netsend-bytes'];
% 
% netbyterecv = changeArray(netbyterecv,10,10);
% plot(curtimestamp,netbyterecv,'m');
% hold on;
% legendList = [legendList,'netrecv-bytes'];

cpupercent = changeArray(cpupercent,10,10);
plot(curtimestamp,cpupercent,'r');
hold on;
legendList = [legendList,'cpu-percent'];

plot(curtimestamp,mempercent,'g+');
hold on;
legendList = [legendList,'memory-percent'];

plot(curtimestamp,diskpercent,'k*');
hold on;
legendList = [legendList, 'disk-percent'];

for i=1:length(logsByAddr);
    plot(logsByAddr(i).timestamp,logsByAddr(i).intervalTime);
    hold on;
    grid on;
    legendList = [legendList,strcat('delay:',logsByAddr(i).addr)];
end;
legend(legendList(1:length(legendList)));
xlabel('timestamp');
ylabel('delay or % of usage');
