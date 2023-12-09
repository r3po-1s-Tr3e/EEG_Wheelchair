function ploterp_diff_all_letters_atoz(date,subject,letter)
    base = 'C:\Users\Vinay\OneDrive - IIT Kanpur\Documents\CurrentStudy\';
    %xdffile = strcat(base,date,'\',subject,'\',letter,'.xdf');
    xdffile = 'C:\Users\Vinay\OneDrive - IIT Kanpur\Documents\P300\LabRecorder\foo.xdf';

    bstfile = strcat(base,'bsts\all_letters.txt');
    chan_locs_file = strcat(base,'channel_locs.ced');
    eventsfile = strcat(base,date,'\',subject,'\',letter,'_all_events.txt');
    bins_saved_in = strcat(base,date,'\',subject,'\',letter,'_all_bins.txt');
    good_channels = get_channels(strcat(base,date,'\',subject,'\','good_channels.txt'));
   
    %basic
    band=[0.1 30];
    time_window=[-200 600];
    
    
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

    EEG  = pop_binlister( EEG , 'BDF', bstfile, 'ExportEL', bins_saved_in, 'IndexEL',  1, 'SendEL2', 'EEG&Text', 'Voutput','EEG' );    
    [ALLEEG ,EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_epochbin( EEG , time_window,  'pre');
    [ALLEEG, ~, ~] = pop_newset(ALLEEG, EEG, 5,'setname','ch1248_0.1to30Hz_elist_bins_epochs','gui','off'); 
    ERP = pop_averager( ALLEEG , 'Criterion', 'good', 'DQ_custom_wins', 0, 'DQ_flag', 1, 'DQ_preavg_txt', 0, 'DSindex', 5, 'ExcludeBoundary',...
     'on', 'SEM', 'on' );
   ERP = pop_binoperator( ERP, {  'Bin53= Bin1 - Bin2 label a-Diff','Bin54= Bin3 - Bin4 label b-Diff','Bin55= Bin5 - Bin6 label c-Diff','Bin56= Bin7 - Bin8 label d-Diff','Bin57= Bin9 - Bin10 label e-Diff','Bin58= Bin11 - Bin12 label f-Diff','Bin59= Bin13 - Bin14 label g-Diff','Bin60= Bin15 - Bin16 label h-Diff','Bin61= Bin17 - Bin18 label i-Diff','Bin62= Bin19 - Bin20 label j-Diff','Bin63= Bin21 - Bin22 label k-Diff','Bin64= Bin23 - Bin24 label l-Diff','Bin65= Bin25 - Bin26 label m-Diff','Bin66= Bin27 - Bin28 label n-Diff','Bin67= Bin29 - Bin30 label o-Diff','Bin68= Bin31 - Bin32 label p-Diff','Bin69= Bin33 - Bin34 label q-Diff','Bin70= Bin35 - Bin36 label r-Diff','Bin71= Bin37 - Bin38 label s-Diff','Bin72= Bin39 - Bin40 label t-Diff','Bin73= Bin41 - Bin42 label u-Diff','Bin74= Bin43 - Bin44 label v-Diff','Bin75= Bin45 - Bin46 label w-Diff','Bin76= Bin47 - Bin48 label x-Diff','Bin77= Bin49 - Bin50 label y-Diff','Bin78= Bin51 - Bin52 label z-Diff'});
   ERP = pop_ploterps( ERP,  53:78,  1:4 , 'AutoYlim', 'on', 'Axsize', [ 0.05 0.08], 'BinNum', 'on', 'Blc', 'pre', 'Box', [ 2 2], 'ChLabel',...
 'on', 'FontSizeChan',  10, 'FontSizeLeg',  12, 'FontSizeTicks',  10, 'LegPos', 'bottom', 'Linespec', {'-r', '--r', ':r', '-.r', '-g', '--g', ':g', '-.g', '-b', '--b', ':b', '-.b', '-c', '--c', ':c', '-.c', '-m', '--m', ':m', '-.m', '-y', '--y', ':y', '-.y', '-k', '--k' },...
 'LineWidth',  1, 'Maximize', 'on', 'Position', [ 103.714 15.9048 106.857 31.9524], 'Style', 'Classic', 'Tag', 'ERP_figure', 'Transparency',...
  0, 'xscale', [ time_window(1) time_window(2)  time_window(1):100:time_window(2) ], 'YDir', 'normal' );