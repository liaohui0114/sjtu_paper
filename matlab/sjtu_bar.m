erasure_20160518_84 = [60.2,60.2;60.3,60.3;60.8,60.9;66.4,66.4;71.8,71.8;80.2,79.9;112.1,110.7;1762.0,1249.6;6505,5116.4;9085.3,7836.6];
erasure_20160518_63 = [60.2,60.2;60.3,60.3;60.7,60.8;65.2,65.3;68.8,69;75,75.3;96.2,90.6;669.3,453;4068,3564.3;8394.6,7747.2];
figure(1);
bar(erasure_20160518_84);
file_list = {'0.png','1.jpg','2.zip','3.zip','4.tar.gz','5.zip','6.deb','7.tgz','8.mkv','9.mkv'};
set(gca,'XTickLabel',file_list);
ylabel('total_dalay=delay(s)*10tims');
grid on;

figure(2);
bar(erasure_20160518_63);
set(gca,'XTickLabel',file_list);
ylabel('total_dalay=delay(s)*10tims');
grid on;