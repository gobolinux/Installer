/*
 * Print partition name and flags *only*, not including any other
 * meta-data whatsoever.
 *
 * Written by Lucas C. Villa Real <lucasvr@gobolinux.org>
 * Released under the GNU GPL version 2 or above.
 */
#include <stdio.h>
#include <parted/parted.h>

int main(int argc, char **argv)
{
	PedPartitionFlag flag = 0;
	PedPartition *part = NULL;
	PedDevice *dev = NULL;
	PedDisk *disk = NULL;
	char *user_dev;
	char buf[128];
	size_t n = sizeof(buf);

	user_dev = argc > 1 ? argv[1] : NULL;

	ped_device_probe_all();
	while ((dev = ped_device_get_next(dev))) {
		if (user_dev && strcmp(user_dev, dev->path))
			continue;
		disk = ped_disk_new(dev);
		while ((part = ped_disk_next_partition(disk, part))) {
			if (part->num < 0)
				continue;
			memset(buf, 0, sizeof(buf));
			snprintf(buf, sizeof(buf)-1, "%s%d:", dev->path, part->num);
			n -= strlen(buf) + 1;
			while ((flag = ped_partition_flag_next(flag))) {
				if (ped_partition_get_flag(part, flag)) {
					if (n > 0) {
						strncat(buf, ped_partition_flag_get_name(flag), n);
						n = sizeof(buf) - strlen(buf) - 1;
					}
					if (n > 0) {
						strncat(buf, ",", n);
						n--;
					}
				}
			}
			if (buf[strlen(buf)-1] == ',')
				buf[strlen(buf)-1] = '\0';
			printf("%s\n", buf);
			flag = 0;
		}
		part = NULL;
		ped_disk_destroy(disk);
	}
	return 0;
}
