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
% 'diamond' or d    Diamondvi
% ^  Upward-pointing triangle
% v   Downward-pointing triangle
% >  Right-pointing triangle
% 'pentagram' or p    Five-pointed star (pentagram)
% 'hexagram' or h     Six-pointed star (hexagram)


%description:to get system information

%%%%%%%%%%%%global variables%%%%%%%%%%%%%%
serverAddr = {'192.168.3.6','192.168.3.7','192.168.3.8'};
%serverAddr = {'192.168.3.6'};
%serverAddr = {'192.168.3.7'};
%serverAddr = {'127.0.0.1'};
server_color = {'g','r','k'}
%serverAddr(3) = cellstr('123')
%serverAddr{3} = 'liaohui';
file_list = {'0.png','1.jpg','2.zip','3.zip','4.tar.gz','5.zip','6.deb','7.tgz','8.mkv','9.mkv'};
%prefix_downinfo = '../log/remote-0504/40-5/scheduled/192.168.3.5/log/';
%prefix_downinfo = '../log/'
%prefix_down_list= {'../log/remote-0508/40-5/normal/192.168.3.5/log/','../log/remote-0504/40-5/scheduled/192.168.3.5/log/'};
%prefix_down_list = {'../log/'};


prefix_downinfo = '../log/remote-0518/weibull-erasurecode-6-3/log/';
prefix_down_list= {'../log/remote-0518/weibull-erasurecode-6-3/log/erasure_code_6_3_normal_','../log/remote-0518/weibull-erasurecode-6-3/log/erasure_code_6_3_scheduled_'};
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
   
   
   
    
    downinfo_name = strcat(prefix_downinfo,'downloadinfo-',file_list{counter},'.txt')
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
        [net_send,net_recv,net_delay,net_timestamp] = textread(strcat(prefix_downinfo,'monitorinfo-',serverAddr{i},'.txt'),'%f\t%f\t%f\t%f',-1);
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

 %%%%%%%to count every single file ''s total time%%%%%%%%%%%
    tmp_total = 0;
    for i=1:length(logsByAddr);
        logsByAddr(i).intervalTime
        tmp_total = tmp_total + sum(logsByAddr(i).intervalTime);
        
    end;
    file_total_time = [file_total_time,tmp_total];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
           
end;

grid on;
legend(legendList(1:length(legendList)));
xlabel('timestamp');
ylabel('delay or % of usage');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



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


total_time = [];

for i=1:length(file_list);
   tmp_total = [];
   for counter=1:length(prefix_down_list);
    tmp_downinfo_name = strcat(prefix_down_list{counter},file_list{i},'.txt');
    
    [start_time,end_time,delay,ip1,ip2,ip3,ip4]=textread(tmp_downinfo_name,'%f%f%f%s%s%s%s');
    delay = sort(delay,1)
    %delay = delay(1:10)
    tmp_downinfo_name
    length(delay)
    tmp_total = [tmp_total,sum(delay)];
   end; 
   total_time = [total_time;tmp_total];

end;
total_time
figure(3);
bar(total_time);
set(gca,'XTickLabel',file_list);
ylabel('total_dalay=delay(s)*50tims');
grid on;







