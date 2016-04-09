function [ systemInfoArray ] = changeArray( systemInfoArray,divider,maxNum )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
while max(systemInfoArray)>maxNum
    systemInfoArray = systemInfoArray/10;
end;

end

% function rtn = getArray(systemInfoArray,divider,maxNum)
% %this is a function to get less array
% while max(systemInfoArray)>maxNum
%     systemInfoArray = systemInfoArray/10;
% end;
% end;