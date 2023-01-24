from joblib import Memory
import numpy as np

cache_dir = "../data/cache_dir"
memory = Memory(cache_dir, verbose=0)


@memory.cache
def generate_allowable_freq_dict(possible_samples_per_message_list, start_freq, end_freq, step_freq):
    result = {}
    print("new settings")

    for samples_per_message in possible_samples_per_message_list:
        print("samples per msg:", samples_per_message)
        result[samples_per_message] = get_all_allowable_freq(samples_per_message, start_freq, end_freq, step_freq)

    return result


def is_allowable_freq(freq, samples_per_message):
    if (samples_per_message * (10 ** 18)) % freq == 0:
        return freq
    else:
        return 0


# def get_all_allowable_freq(samples_per_message, start_freq, end_freq, step_freq):
#     possible_frequencies = np.arange(start_freq, end_freq, step_freq)
#     samples_per_message_array = np.zeros(possible_frequencies.size, dtype=np.int16) + samples_per_message
#     # result = np.empty(possible_frequencies.size, dtype=np.int64)
#
#     num_chunks = 14 * 40
#     chunk_size = max(1, possible_frequencies.size // num_chunks)
#
#     with ProcessPoolExecutor() as executor:
#         generator = executor.map(is_allowable_freq,
#                                  possible_frequencies,
#                                  samples_per_message_array,
#                                  chunksize=chunk_size)
#
#         # for i, freq in enumerate(generator):
#         #     result[i] = freq
#         result = np.array(list(generator), dtype=np.int64)
#
#     return result[result != 0]

@memory.cache
def get_all_allowable_freq(samples_per_message, start_freq, end_freq, step_freq):
    return [freq for freq in range(start_freq, end_freq, step_freq) if (samples_per_message * (10 ** 18)) % freq == 0]


if __name__ == "__main__":
    import time

    print("list")

    results = []

    for _ in range(10):
        start = time.time()
        a = get_all_allowable_freq(60, 1, 400000000, 1000)
        end = time.time()
        results.append(end-start)
    print(results)

    print("max", max(results), "min", min(results), "avg", sum(results) / len(results))
