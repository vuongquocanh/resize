import os
import cv2
from sqlalchemy import create_engine, text

from resize import generate_avatar_path_v2  # Assuming this is a custom function you have defined

path = 'Archive'
unitcode = 'U01.1.100'
path_save = r'X:/APP_POS/ImageVatTu/' + unitcode
url_avt = f'APP_POS/ImageVatTu/{unitcode}/'

engine = create_engine('postgresql://fepvector:Admincati123654@10.192.4.10:27600/MART')
conn = engine.connect()

files = 0
folders = 0

for root, dirnames, filenames in os.walk(path):
    dirnames.extend([name.split(".")[0] for name in filenames])

    for directory in dirnames:
        dir_path = os.path.join(path_save, directory + "." + unitcode)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        folders += 1

    for filename in filenames:
        file_path = os.path.join(root, filename)
        try:
            image = cv2.imread(file_path)
            if image is None:
                print(f"Error: Could not read {file_path}. Skipping...")
                continue

            folder = filename.split(".")[0] + "." + unitcode
            avatar = url_avt + folder + "/" + filename
            # update db
            update_query = text('update "SELL".dm_vattu set avartar = :avatar where mavattupk = :mavtpk')
            new_data = {"avartar": avatar, "mavtpk": folder}
            conn.execute(update_query, new_data)

            output_folder = os.path.join(path_save, folder)
            output_file_path = os.path.join(output_folder, filename)

            if not os.path.exists(output_folder):
                os.mkdir(output_folder)

            if not os.path.exists(output_file_path):
                cv2.imwrite(output_file_path, image)
                print(f"Saved {output_file_path}")

            # Assuming generate_avatar_path_v2 takes image, output_folder, and filename
            generate_avatar_path_v2(image, output_folder, filename)

            files += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

print("{:,} files, {:,} folders processed.".format(files, folders))
