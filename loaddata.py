from tqdm import tqdm
import brain_observatory_utilities.datasets.optical_physiology.data_formatting as ophys_formatting
import pandas as pd

def get_experiments(
    cache,
    structures=None,      # List of structures you want data from
    reporters=None,       # List of reporter lines you want data from
    image_sets=None,      # List of image_sets you want data from
    cre_lines=None,       # List of cre_lines you want data from
    passive=None,         # Boolean for whether you want passive session data
    experience=None,      # Str for 'familiar' or 'novel' imaging sessions
    unique_session=False, # Boolean for choosing 1 specific session (automatically chooses the session with the most data)
    unique_mouse=False,   # Boolean for choosing 1 specific mouse (automatically chooses the mouse with the most data)
    mouse_offset=0,
    download_image = False,
):
    if structures is not None: assert type(structures) == list, f"Invalid Arg: 'structures' must be list of str"
    if reporters is not None: assert type(reporters) == list, f"Invalid Arg: 'reports' must be list of str"
    if image_sets is not None: assert type(image_sets) == list, f"Invalid Arg: 'image_sets' must be list of str"
    if cre_lines is not None: assert type(cre_lines) == list, "Invalid Arg: 'cre line' must be str"
    if passive is not None: assert type(passive) == bool, f"Invalid Arg: 'passive' must be True or False"
    if experience is not None: assert type(experience) == str and experience in ['familiar', 'novel'], f"Invalid Arg: 'experience' must be one of ['familiar', 'novel']"
    if unique_session is not None: assert type(unique_session) == bool, "Invalid Arg: 'unique_session must be bool"
    if unique_mouse is not None: assert type(unique_mouse) == bool, "Invalid Arg: 'unique_mouse must be bool"

    exp_set = cache.get_ophys_experiment_table()
    if structures is not None: exp_set = exp_set[exp_set['targeted_structure'].isin(structures)]
    if reporters is not None: exp_set = exp_set[exp_set['reporter_line'].isin(reporters)]
    if image_sets is not None: exp_set = exp_set[exp_set['image_set'].isin(image_sets)]
    if cre_lines is not None: exp_set = exp_set[exp_set['cre_line'].isin(cre_lines)]
    if passive is not None: exp_set = exp_set[exp_set['passive'] == passive]
    if experience is not None: exp_set = exp_set[exp_set['experience_level'] == experience]

    if unique_session:
        session_id = exp_set['ophys_session_id'].value_counts().keys()[0]
        exp_set = exp_set[exp_set['ophys_session_id'] == session_id]

    if unique_mouse:
        mouse_id = exp_set['mouse_id'].value_counts().keys()[mouse_offset]
        exp_set = exp_set[exp_set['mouse_id'] == mouse_id]

    experiment_ids = exp_set.index
    print(f"loading {len(experiment_ids)} experiments.")

    experiments = {}
    for id in experiment_ids:
      experiments[id] = cache.get_behavior_ophys_experiment(id)
      if not download_image:
        del experiments[id]._stimuli._templates

    return experiments, experiment_ids

def get_neural_data(experiments):
    neural_data = []
    for ophys_experiment_id in tqdm(experiments.keys()): #tqdm is a package that shows progress bars for items that are iterated over
        this_experiment = experiments[ophys_experiment_id]
        this_experiment_neural_data = ophys_formatting.build_tidy_cell_df(this_experiment)

        # add some columns with metadata for the experiment
        metadata_keys = [
          'ophys_experiment_id',
          'ophys_session_id',
          'targeted_structure',
          'imaging_depth',
          'equipment_name',
          'cre_line',
          'mouse_id',
          'sex',
        ]
        for metadata_key in metadata_keys:
            this_experiment_neural_data[metadata_key] = this_experiment.metadata[metadata_key]

        # append the data for this experiment to a list
        neural_data.append(this_experiment_neural_data)

    # concatate the list of dataframes into a single dataframe
    neural_data = pd.concat(neural_data)
    return neural_data