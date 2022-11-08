import gym
import logging
import multiprocessing
import faulthandler

faulthandler.enable()
from gym_dssat_pdi.envs.utils import utils
import os

import numpy as np
from copy import deepcopy
from pprint import pprint

import os

dirname = os.path.dirname(__file__)
auxfiles_path = os.path.join('/opt/gym_dssat_pdi/samples', 'test_files/GAGR.CLI')


def interact_with_env(env, verbose=True):
    interactions = []
    i = 0
    while not env.done:
        observation = env.observation
        print(">>> iteration ",i)
        print('state: ', observation)
        observation_list = env.observation_dict_to_array(observation)
        dap = observation['dap']
        action = input("action(anfer,amir) > ")
        anfer, amir = [int(v) for v in str.split(action,",")]
        action = {'anfer': anfer, 'amir': amir}
        res = env.step(action)
        new_state, reward, done, info = res
        print("action: ",action)
        print("reward: ",reward)
        if new_state is not None:
            interactions.append(new_state)
        i += 1
    return interactions

if __name__ == '__main__':
    dir = './logs/'
    utils.make_folder(dir)
    try:
        for file in os.scandir(dir):
            os.remove(file.path)
    except:
        pass
    utils.make_folder('./render')
    cwd = os.path.dirname(os.path.realpath(__file__))
    mode = 'fertilization'

    print(f'MODE: {mode}')
    env_args = {
        'run_dssat_location': '/opt/dssat_pdi/run_dssat',
        'log_saving_path': './logs/dssat_pdi.log',
        'mode': mode,
        'seed': 123456,
        'random_weather': True,
        'auxiliary_file_paths': [auxfiles_path],
    }
    try_interact = True
    try_multiproc = True
    verbose = True
    if try_interact:
        try:
            env = gym.make('gym_dssat_pdi:GymDssatPdi-v0', **env_args)
            env.get_env_info(user_input=False)
            env.seed(123)
            yields = []
            while True:
                env.reset()
                interactions = interact_with_env(env, verbose=verbose)
                yields.append(interactions[-1]['grnwt'])
                if (j + 1) % 10 == 0:
                    print(f'{j + 1}/{n_rep}')
            print(f'mean of yields: {np.mean(yields)} kg/ha')
            print(f'variance of yields: {np.var(yields)} kg/ha')
            if mode == 'mode':
                env.render(type='ts',
                            feature_name_1='cleach',
                            feature_name_2='totaml')
                env.render(type='reward',
                            cumsum=True)
                env.render(type='reward',
                            cumsum=False)
            env.reset_hard()
        except Exception as e:
            logging.exception(e)
        finally:
            env.close()
