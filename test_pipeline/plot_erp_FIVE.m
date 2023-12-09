
function plot_erp_FIVE(filename,c1,c2,c3,c4,letter)
    right_channels = [str2num(c1) str2num(c2) str2num(c3) str2num(c4)];
    disp(class(right_channels))
    
    disp(right_channels)
    base = 'C:\Users\vinay\Documents\test_pipeline\';
    datafile = 'C:\Users\vinay\Downloads\LabRecorder-1.16.2-Win_amd64\LabRecorder\foo.xdf';
    bstfile = strcat(base,'5_bsts\5_',letter,'.txt');
    chan_locs_file = strcat(base,'channel_locs.ced');
    eventsfile = strcat(base,'events','\',filename,'_events.txt');
    bins_saved_in = strcat(base,'bins','\',filename,'_bins.txt');
    erp_saved_in = strcat(base,'erps','\');
    time_window=[-200 400];
    
   [ALLEEG EEG CURRENTSET ALLCOM] = eeglab('nogui');
    EEG = pop_loadxdf(datafile , 'streamtype', 'EEG', 'exclude_markerstreams', {});
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 
    EEG = eeg_checkset( EEG );
    EEG = pop_select( EEG, 'channel',right_channels );
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'gui','off'); 
    EEG = eeg_checkset( EEG );
    EEG=pop_chanedit(EEG, 'load',{chan_locs_file,'filetype','autodetect'});
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_eegfiltnew(EEG, 'locutoff',8,'hicutoff',35);
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'gui','off'); 
    EEG = eeg_checkset( EEG );
    %pop_eegplot( EEG, 1, 1, 1);
    EEG  = pop_creabasiceventlist( EEG , 'AlphanumericCleaning', 'on', 'BoundaryNumeric', { -99 }, 'BoundaryString', { 'boundary' }, 'Eventlist', eventsfile ); % GUI: 28-Nov-2022 15:18:06
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 3,'gui','off'); 
    EEG  = pop_binlister( EEG , 'BDF', bstfile, 'ExportEL', bins_saved_in, 'IndexEL',  1, 'SendEL2', 'EEG&Text', 'Voutput', 'EEG' ); % GUI: 28-Nov-2022 15:18:31
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_epochbin( EEG , [-200.0  800.0],  'pre'); % GUI: 28-Nov-2022 15:18:41
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 5,'gui','off');
    ERP = pop_averager( ALLEEG , 'Criterion', 'good', 'DQ_custom_wins', 0, 'DQ_flag', 1, 'DQ_preavg_txt', 0, 'DSindex', 5, 'ExcludeBoundary',...
     'on', 'SEM', 'on' );
    ERP = pop_ploterps( ERP, [ 1 2],  1:4 , 'AutoYlim', 'on', 'Axsize', [ 0.05 0.08], 'BinNum', 'on', 'Blc', 'pre', 'Box', [ 2 2], 'ChLabel',...
     'on', 'FontSizeChan',  10, 'FontSizeLeg',  12, 'FontSizeTicks',  10, 'LegPos', 'bottom', 'Linespec', {'k-' , 'r-' }, 'LineWidth',  1, 'Maximize',...
     'on', 'Position', [ 103.714 15.9048 106.857 31.9524], 'Style', 'Classic', 'Tag', 'ERP_figure', 'Transparency',  0, 'xscale',...
     [ time_window(1) time_window(2)   time_window(1):100:time_window(2) ], 'YDir', 'normal' );