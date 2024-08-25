import os
import pandas as pd
from matplotlib import pyplot as plt


def analyze_results_and_generate_plot(filename, maze_size, logger, show=False, start_end_in_the_same_q=False):
    # Custom weights emphasizing path cost and searched cells percentage
    weights = {
        'exec_time': 0.2,
        'searched_cells': 0.40,
        'path_cost': 0.40
    }

    # Display maze size in the console
    logger.info(f"Analyzing maze of size: {maze_size}x{maze_size}")

    # Load the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        return

    # Summarize the data by algorithm
    summary = df.groupby('Algorithm_name').agg(
        avg_exec_time=('Execution Time (s)', 'mean'),
        avg_searched_cells=('Searched Cells', 'mean'),
        avg_path_cost=('Total Path Cost', 'mean')
    ).reset_index()

    # Apply weights before multiplying or dividing
    summary['weighted_exec_time'] = summary['avg_exec_time'] * weights['exec_time']
    summary['weighted_searched_cells'] = summary['avg_searched_cells'] * weights['searched_cells']
    summary['weighted_path_cost'] = summary['avg_path_cost'] * weights['path_cost']

    # Calculate overall score by multiplying all weighted metrics together
    summary['overall_score'] = round((
            summary['weighted_exec_time'] *
            summary['weighted_searched_cells'] *
            summary['weighted_path_cost']
    ), 3)

    # Sort by overall score (lower scores are better)
    summary = summary.sort_values('overall_score')

    # Rank the algorithms based on the sorted overall score (1 for best score)
    summary['overall_rank'] = summary['overall_score'].rank(method='min')

    # Log the ranked summary
    logger.info("Ranked Algorithm Performance (Using Multiplication for Overall Score):")
    logger.info(
        f"\n{summary[['Algorithm_name', 'avg_exec_time', 'avg_searched_cells', 'avg_path_cost', 
                      'overall_score', 'overall_rank']].to_string(index=False)}\n")

    # Generate Charts
    generate_charts(summary, show, maze_size, start_end_in_the_same_q)


def generate_charts(summary, show, maze_size, start_end_in_the_same_q):
    folder_name = f"maze_{maze_size}"

    def get_file_path(filename):
        return os.path.join(folder_name, f"{filename}_{maze_size}_{start_end_in_the_same_q}.png")

    # Ensure the directory exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    plt.figure(figsize=(10, 6))
    plt.bar(summary['Algorithm_name'], summary['avg_exec_time'], color='blue')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Execution Time (s)')
    plt.title(f'Average Execution Time by Algorithm (Maze Size: {maze_size})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(get_file_path('avg_execution_time'))
    if show:
        plt.show()
    else:
        plt.close()  # Close the figure only if not showing it

    plt.figure(figsize=(10, 6))
    plt.bar(summary['Algorithm_name'], summary['avg_searched_cells'], color='orange')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Searched Cells')
    plt.title(f'Average Searched Cells by Algorithm (Maze Size: {maze_size})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(get_file_path('avg_searched_cells'))
    if show:
        plt.show()
    else:
        plt.close()  # Close the figure only if not showing it

    plt.figure(figsize=(10, 6))
    plt.bar(summary['Algorithm_name'], summary['avg_path_cost'], color='red')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Path Cost')
    plt.title(f'Average Path Cost by Algorithm (Maze Size: {maze_size})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(get_file_path('avg_path_cost'))
    if show:
        plt.show()
    else:
        plt.close()  # Close the figure only if not showing it

    plt.figure(figsize=(10, 6))
    plt.bar(summary['Algorithm_name'], summary['overall_rank'], color='purple')
    plt.xlabel('Algorithm')
    plt.ylabel('Overall Rank')
    plt.title(f'Overall Rank by Algorithm (Maze Size: {maze_size})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(get_file_path('overall_rank'))
    if show:
        plt.show()
    else:
        plt.close()  # Close the figure only if not showing it
