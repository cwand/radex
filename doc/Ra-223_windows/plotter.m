clear all; close all; clc;

d = importdata("C:\Users\bub8ga\pyspec\DICOM\spectra\kilde 2\kilde 2.txt","\t",2);
data = d.data;

ralines = [81.1,83.8,94.2,94.9,97.5,122,144,154,269,324,338,445];
rnlines = [271,402];
bilines = [351];
pblines = [405,427];

w1 = 76:89;
y1 = data(77:90,2);
area(w1,y1,'FaceColor',[0.7,0.7,0.7]); hold on;
w2 = 133:165;
y2 = data(134:166,2);
area(w2,y2,'FaceColor',[0.7,0.7,0.7]);
w3 = 255:283;
y3 = data(256:284,2);
area(w3,y3,'FaceColor',[0.7,0.7,0.7]);
w4 = 322:366;
y4 = data(323:367,2);
area(w4,y4,'FaceColor',[0.7,0.7,0.7]);
w5 = 383:422;
y5 = data(384:423,2);
area(w5,y5,'FaceColor',[0.7,0.7,0.7]);



ra = plot([ralines(1),ralines(1)],[0,23000],'linewidth',2,'Color',[0.9290 0.6940 0.1250]);
rn = plot([rnlines(1),rnlines(1)],[0,23000],'linewidth',2,'Color',[0 0.4470 0.7410]);
bi = plot([bilines(1),bilines(1)],[0,23000],'linewidth',2,'Color',[0.4660 0.6740 0.1880]);
pb = plot([pblines(1),pblines(1)],[0,23000],'linewidth',2,'Color',[0.4940 0.1840 0.5560]);

for i = 2:length(ralines)
	plot([ralines(i),ralines(i)],[0,23000],'color',ra.Color,'linewidth',2)
end
plot([rnlines(2),rnlines(2)],[0,23000],'color',rn.Color,'linewidth',2);
plot([pblines(2),pblines(2)],[0,23000],'color',pb.Color,'linewidth',2);

sp = plot(data(:,1),data(:,2),'k-','linewidth',2);

ylim([0 25000])

xlabel('E [keV]','interpreter','latex')
ylabel('Counts','interpreter','latex')

set(gca,'TickLabelInterpreter','latex');

legend([ra,rn,bi,pb,sp],{'Ra-223','Rn-219','Bi-211','Pb-211'},'interpreter','latex')

