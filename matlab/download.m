
%logfiles = dir(fullfile('../log/downloadinfo-*.txt')); % to get all log file named downloadinfo_*.txt
logfiles = dir(fullfile('../logs-everyday/20160409/agent/log/downloadinfo-*.txt')); % to get all log file named downloadinfo_*.txt
fileCounter = length(logfiles);


pathPrefix = 'downloadinfo-';
pathPostfix = '.txt';
for i = 1:fileCounter;
    %logfilenames(i).name = strcat('../log/',logfiles(i).name);  %to get filenames list
    logfilenames(i).name = strcat('../logs-everyday/20160409/agent/log/',logfiles(i).name);  %to get filenames list
end

c = rand(fileCounter,3); %random color

legendList = {};
for i = 1:fileCounter;
    logfiles(i).name;
    [start_time,end_time,intervalTime,filename,filesize,server_ip]=textread(logfilenames(i).name,'%f%f%f%s%f%s',-1);

    plot(start_time,intervalTime,'color',c(i,:));
    hold on
    grid on
    
    tmp = logfiles(i).name
    tmp = tmp(length(pathPrefix)+1:findstr(tmp,pathPostfix)-1);
    tmp = strcat(tmp,':',num2str(filesize(1)));
    legendList =[legendList,tmp];
end
xlabel('timestamp')
ylabel('interval Time')
legend(legendList(1:fileCounter));


