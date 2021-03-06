import click
from cot.backend.manage import stack as manage_stack_backend


@click.command(
    'stack',
    short_help='Manage a CloudFormation stack',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-d',
    '--delete',
    help='delete the stack',
    is_flag=True
)
@click.option(
    '-i',
    '--stack-initiate',
    is_flag=True,
    help='initiate but do not monitor the stack operation(disable monitoring)',
)
@click.option(
    '-m',
    '--stack-monitor',
    is_flag=True,
    help='monitor but do not initiate the stack operation(disable initiation)'
)
@click.option(
    '-w',
    '--stack-wait',
    type=click.INT,
    show_default=True,
    default=30,
    help='interval between checking the progress of the stack operation'
)
@click.option(
    '-n',
    '--stack-name',
    default=None,
    help='override standard stack naming'
)
@click.option(
    '-l',
    '--level',
    type=click.Choice(
        [
            'account',
            'product',
            'segment',
            'solution',
            'application',
            'multiple'
        ],
        case_sensitive=False
    ),
    help='stack level',
    required=True
)
@click.option(
    '-r',
    '--region',
    help='AWS region identifier for the region in which the stack should be managed'
)
@click.option(
    '-u',
    '--deployment-unit',
    help='deployment unit used to determine the stack template',
    required=True
)
@click.option(
    '-z',
    '--deployment-unit-subset',
    help='subset of the deployment unit required'
)
@click.option(
    '-y',
    '--dryrun',
    is_flag=True,
    help='show what will happen without actually updating the stack'
)
def stack(**kwargs):
    """
    Manage a CloudFormation stack

    \b
    NOTES:
    1. You must be in the correct directory corresponding to the requested stack level
    2. REGION is only relevant for the "product" level, where multiple product stacks are necessary
       if the product uses resources in multiple regions
    3. "segment" is now used in preference to "container" to avoid confusion with docker
    4. If stack doesn't exist in AWS, the update operation will create the stack
    5. Overriding the stack name is not recommended except where legacy naming has to be maintained
    6. A dryrun creates a change set, then displays it. It only applies when
       the STACK_OPERATION=update
    """
    manage_stack_backend.run(**kwargs, _is_cli=True)
