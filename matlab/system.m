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

%%%%%%%%%%%%global variables%%%%%%%%%%%%%%
%serverAddr = {'192.168.3.6','192.168.3.7'};
%serverAddr = {'192.168.3.6'};
%serverAddr = {'192.168.3.7'};
serverAddr = {'127.0.0.1'};
server_color = {'g','r'}
%serverAddr(3) = cellstr('123')
%serverAddr{3} = 'liaohui';
file_list = {'0.png','1.jpg','2.zip','3.zip','4.tar.gz','5.zip','6.deb','7.tgz','8.mkv','9.mkv'};
%prefix_downinfo = '../log/remote-0429/40/normal/192.168.3.5/log/';
prefix_downinfo = '../log/'
%prefix_down_list= {'../log/remote-0429/80/normal/192.168.3.5/log/','../log/remote-0429/80/scheduled/192.168.3.5/log/'};
prefix_down_list = {'../log/'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
file_total_time = [];

%init logsByAddr
for i=1:length(serverAddr);
        logsByAddr(i).addr = serverAddr{i};
        logsByAddr(i).timestamp = [];
        logsByAddr(i).intervalTime = [];
end;
   
  
for counter=1:length(file_list);
    
    

     for i=1:length(serverAddr);
        logsByAddr(i).addr = serverAddr{i};
        logsByAddr(i).timestamp = [];
        logsByAddr(i).intervalTime = [];
    end;
   
   
   
    
    downinfo_name = strcat(prefix_downinfo,'downloadinfo-',file_list{counter},'.txt');
    fid = fopen(downinfo_name);
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
        
        
    end;

    


    


    legendList = {};
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     figure(1); %graph 1
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subplot(4,3,counter);  %draw sub plot
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%monitor info%%%%
    for i=1:length(serverAddr);
        [net_send,net_recv,net_delay,net_timestamp] = textread(strcat(prefix_downinfo,'monitorinfo-',serverAddr{i},'.txt'),'%f\t%f\t%f\t%f',-1)
        net_send = changeArray(net_send,10,100); %lower than 100
        plot(net_timestamp,net_send,server_color{i});
        hold on;
        legendList = [legendList,strcat(serverAddr{i},':net_send')];
    end;

   
    for i=1:length(logsByAddr);
        logsByAddr(i).timestamp
        plot(logsByAddr(i).timestamp,logsByAddr(i).intervalTime,strcat(server_color{i},'*'));
        hold on;

        legendList = [legendList,strcat('delay:',logsByAddr(i).addr)];
    end;
    
    xlabel(file_list{counter}); %xlabel of every subplot:filename

 %%%%%%%to count every single file's total time%%%%%%%%%%%
    tmp_total = 0;
    for i=1:length(logsByAddr);
        logsByAddr(i).intervalTime
        tmp_total = tmp_total + sum(logsByAddr(i).intervalTime)
        
    end;
    file_total_time = [file_total_time,tmp_total];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
           
end;

grid on;
legend(legendList(1:length(legendList)));
xlabel('timestamp');
ylabel('delay or % of usage');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



file_total_time
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bar_list = [];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure(2); %graph 2
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bar(file_total_time);
set(gca,'XTickLabel',file_list);
ylabel('delay(s)');
grid on;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%









%%%%%%%%to get total time of every%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

total_time_by_ip = [];
for counter=1:length(prefix_down_list);
    tmp_total = 0;
   for i=1:length(file_list);
    tmp_downinfo_name = strcat(prefix_down_list{counter},'downloadinfo-',file_list{i},'.txt');
    
    [start_time,end_time,intervalTime,filename,filesize,server_ip]=textread(tmp_downinfo_name,'%f%f%f%s%f%s');
    tmp_total = tmp_total+sum(intervalTime);
   end; 
   total_time_by_ip = [total_time_by_ip,tmp_total];
end;

figure(3);
bar(total_time_by_ip);
grid on;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%{

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
figure(3); %graph 3
bar(file_total_time);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

pre_storage = '/logs-everyday/20160409/storage2';
[curtimestamp1,cpupercent1,mempercent1,diskpercent1,diskread1,diskwrite1,diskreadbyte1,diskwritebyte1,netbytesend1,netbyterecv1] = textread('../log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);
[curtimestamp2,cpupercent2,mempercent2,diskpercent2,diskread2,diskwrite2,diskreadbyte2,diskwritebyte2,netbytesend2,netbyterecv2] = textread('../log/systeminfo.txt','%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);


netsendsum1 = sum(netbytesend1)/(curtimestamp1(end)-curtimestamp1(1))
diskreadsum1 = sum(diskread1)
intervalsum1 = sum(logsByAddr(1).intervalTime)
len1 = length(logsByAddr(1).intervalTime)

netsendsum2 = sum(netbytesend2)/(curtimestamp2(end)-curtimestamp2(1))
diskreadsum2 = sum(diskread2)
intervalsum2 = sum(logsByAddr(2).intervalTime)
len2 = length(logsByAddr(2).intervalTime)


subplot(1,2,1);
bar([netsendsum1/1000,diskreadsum1,intervalsum1;netsendsum2/1000,diskreadsum2,intervalsum2]);
legend('disk-read-total','interval-time-total');
set(gca,'XTickLabel',{'storage1','storage2'});
xlabel('storage1 storage2');
grid on;
%}


%{
%%%%don't know
    
    [curtimestamp,cpupercent,mempercent,diskpercent ,diskread,diskwrite,diskreadbyte,diskwritebyte,netbytesend,netbyterecv] = textread(strcat(prefix_downinfo,'systeminfo.txt'),'%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t',-1);

    legendList = {};

    diskreadbyte = changeArray(diskreadbyte,10,100); %lower than 100

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     figure(1); %graph 1
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
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
%}
