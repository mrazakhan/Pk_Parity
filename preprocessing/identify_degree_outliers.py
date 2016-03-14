import graphlab
import csv
import argparse
from graphlab import degree_counting
'''
#TODO
Make in and out file customizable
Make Caller ID and Receiver ID customizable

'''
def outlier_vertices_list(input_file, output_file, debug_file='debug.txt'):
    data=graphlab.SFrame.read_csv(input_file, header=False, delimiter='|')
    data.rename({'X2':'__src_id','X3':'__dst_id'})

    # Ordering the data according to src id and dest id and then removing duplicates
    data=data['__src_id','__dst_id'].flat_map(['__src_id','__dst_id'],lambda x: [[x['__src_id'],x['__dst_id']] if x['__src_id']<x['__dst_id'] else [x['__dst_id'],x['__src_id']]])

    data=data.unique()

    graph=graphlab.SGraph(edges=data)
    deg = degree_counting.create(graph)
    graph.vertices['total_degree'] = deg['graph'].vertices['total_degree']
    percentile_95=graph.vertices['total_degree'].sketch_summary().quantile(0.95)
    graph.vertices['outlier']=graph.vertices['total_degree'].apply(lambda x:1 if x>=percentile_95 else 0)

    non_outlier_vertices=graph.vertices[graph.vertices['outlier']==0]
    outlier_vertices=graph.vertices[graph.vertices['outlier']==1]

    fout=open(debug_file,'w')
    fout.write('95th Degree Percentile {}\n'.format(percentile_95))
    fout.write('NonOutliers sframe shape {}\n'.format(non_outlier_vertices.shape[0]))
    fout.write('Outliers sframe shape {}\n'.format(outlier_vertices.shape[0]))
    fout.close()

    non_outlier_vertices.save(output_file, format='csv')

if __name__=='__main__':
    '''
    parser=argparse.ArgumentParser(description='Filter outliers by degree')
    parser.add_argument('-if', '--input_file_name', help='mobile money file', required=True)
    parser.add_argument('-ui', '--user_index', help='UserId Index', required=True)
    parser.add_argument('-di', '--date_index', help='Date Index', required=True)
    parser.add_argument('-ct', '--cdr_type', help='cdr type Ghana, Zambia or Pakistan', required=True)
    parser.add_argument('-of', '--output_file_name', help='output file', required=True)
    parser.add_argument('-st_date', '--start_date', help='start date YYYYmmdd format', required=True)
    parser.add_argument('-end_date', '--end_date', help='end date', required=True)

    args = parser.parse_args()
    '''
    input_file='/scratch/raza/MigrationNetworks/0602-Call.pai.sordate.txt'
    output_file='./0602_non_outlier_nodes.txt'
    outlier_vertices_list(input_file, output_file)
