import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
user_data = pd.read_csv('fcc-forum-pageviews.csv')
df = pd.DataFrame(data=user_data)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df.index, df['value'], 'r', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Group and reshape data
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Order months correctly
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar = df_bar[month_order]
    
    # Create plot
    fig = df_bar.plot.bar(figsize=(10, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=month_order)
    plt.tight_layout()
    
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Ensure correct month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Year-wise box plot (Trend)
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_ylim(0, 200000)
    ax1.set_yticks(range(0, 200001, 20000))
    
    # Month-wise box plot (Seasonality)
    sns.boxplot(
        data=df_box, 
        x='month', 
        y='value', 
        order=month_order,
        ax=ax2
    )
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_ylim(0, 200000)
    ax2.set_yticks(range(0, 200001, 20000))
    
    plt.tight_layout()
    fig.savefig('box_plot.png')
    return fig