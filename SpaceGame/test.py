import noise
import helper

n = 10000
scale = 30
minn = 0
maxn = 0
noise_list = []
noise_list2 = []

for i in range(n):
    noise_val = noise.pnoise1(i/scale)
    mapped_noise_val = helper.map_value_to_range(noise_val, -1, 1, 0, 1)
    noise_list.append(noise_val)
    noise_list2.append(mapped_noise_val)

    if (0):
        print(noise_val)

print(max(noise_list))
print(min(noise_list))
print(sum(noise_list)/len(noise_list))

print(max(noise_list2))
print(min(noise_list2))
print(sum(noise_list2)/len(noise_list2))