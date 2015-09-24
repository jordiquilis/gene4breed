import uuid
import os


def create_fasta_file(plants_info):
    output_file_name = os.path.join('/tmp', 'fasta_%s' % str(uuid.uuid4()))
    with open(output_file_name, 'w') as output:
        for plant_info in plants_info:
            if len(plant_info['markers'].keys()):
                output.write(('>%s' % plant_info['plant_name']) + os.linesep)
                values = []
                for marker_name in sorted(plant_info['markers'].keys()):
                    value = plant_info['markers'][marker_name]
                    if value == 'nd' or value=='ND':
                        value = '-'
                    values.append(value)
                output.write(''.join(values) + os.linesep + os.linesep)
    return output_file_name
