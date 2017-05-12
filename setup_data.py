from process_data import process_adv, process_awac
import pull_data as pull

#pull.main()
process_adv({'NREL': 'TTM_NRELvector_Jun2012'}, savefiles=False)
#process_awac(savefiles=False)
