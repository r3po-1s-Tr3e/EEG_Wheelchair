function ploterp_diff(date,subject,letter)
    base = 'C:\Users\Vinay\OneDrive - IIT Kanpur\Documents\CurrentStudy\';
    xdffile = strcat(base,date,'\',subject,'\',letter,'.xdf');
    bstfile = strcat(base,'bsts\',letter,'.txt');
    chan_locs_file = strcat(base,'channel_locs.ced');
    eventsfile = strcat(base,date,'\',subject,'\',letter,'_events.txt');
    bins_saved_in = strcat(base,date,'\',subject,'\',letter,'_bins.txt');
    good_channels = get_channels(strcat(base,date,'\',subject,'\','good_channels.txt'));
   
    %basic
    band=[0.1 30];
    time_window=[-200 400];
    
    
    [ALLEEG, ~ ,~, ~] = eeglab('nogui');
    EEG = pop_loadxdf(xdffile , 'streamtype', 'EEG', 'exclude_markerstreams', {});
    [ALLEEG, EEG, ~] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 
    EEG = eeg_checkset( EEG );
    EEG = pop_select( EEG, 'channel',good_channels);
   [ALLEEG ,EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'setname','ch1248','gui','off'); 
    EEG = eeg_checkset( EEG );
    EEG=pop_chanedit(EEG, 'load',{chan_locs_file,'filetype','autodetect'});
   [ALLEEG, EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_eegfiltnew(EEG, 'locutoff',band(1),'hicutoff',band(2),'plotfreqz',0);
  [ALLEEG, EEG, ~] = pop_newset(ALLEEG, EEG, 2,'setname','ch1248_0.1to30Hz','gui','off'); 
    EEG  = pop_creabasiceventlist( EEG , 'AlphanumericCleaning', 'on', 'BoundaryNumeric', { -99 }, 'BoundaryString', { 'boundary' }, 'Eventlist', eventsfile ); % GUI: 23-Oct-2022 10:52:23
    [ALLEEG, EEG ,CURRENTSET] = pop_newset(ALLEEG, EEG, 3,'gui','off'); 
    EEG  = pop_binlister( EEG , 'BDF', bstfile, 'ExportEL', bins_saved_in, 'IndexEL',  1, 'SendEL2', 'EEG&Text', 'Voutput', 'EEG' ); % GUI: 23-Oct-2022 10:53:07
    [ALLEEG ,EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_epochbin( EEG , time_window,  'pre');
    [ALLEEG, ~, ~] = pop_newset(ALLEEG, EEG, 5,'setname','ch1248_0.1to30Hz_elist_bins_epochs','gui','off'); 
    ERP = pop_averager( ALLEEG , 'Criterion', 'good', 'DQ_custom_wins', 0, 'DQ_flag', 1, 'DQ_preavg_txt', 0, 'DSindex', 5, 'ExcludeBoundary',...
     'on', 'SEM', 'on' );
    ERP = pop_binoperator( ERP, { 'Bin3 = Bin1 - Bin2 label Diff'});
    ERP = pop_ploterps( ERP, [ 3],  1:4 , 'AutoYlim', 'on', 'Axsize', [ 0.05 0.08], 'BinNum', 'on', 'Blc', 'pre', 'Box', [ 2 2], 'ChLabel',...
     'on', 'FontSizeChan',  10, 'FontSizeLeg',  12, 'FontSizeTicks',  10, 'LegPos', 'bottom', 'Linespec', {'k-' , 'r-' }, 'LineWidth',  1, 'Maximize',...
     'on', 'Position', [ 103.714 15.9048 106.857 31.9524], 'Style', 'Classic', 'Tag', 'ERP_figure', 'Transparency',  0, 'xscale',...
     [ time_window(1) time_window(2)   time_window(1):100:time_window(2) ], 'YDir', 'normal' );