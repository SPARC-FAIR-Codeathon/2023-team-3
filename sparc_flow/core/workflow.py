from scriptcwl import WorkflowGenerator
import subprocess
import os

class Workflow(WorkflowGenerator):     
    """ 
    Workflow class for generating CWL workflows.  

    Parameters 
    ---------- 
    language : str, optional 
        Language of workflow. Currently only CWL is supported. 

    Attributes  

    Methods 
    ------- 
    set_steps(tool_path) 
        Sets the steps of the workflow, e.g. path tool Python scripts and CWL files.
    
    set_input_value(input_value, input_name, input_type) 
        Sets the input value of the workflow. 

    generate_description() 
        Generates the description of the workflow, e.g. creates the CWL file. 
    
    run() 
        Runs the workflow, e.g. runs the CWL file.
    ----------
    """ 
    def __init__(self, language="cwl"):   
        super().__init__()
        if language == "cwl": 
            pass
        else: 
            raise NotImplementedError("Only CWL is supported at this time.")    
        
        self.input_step = None
        self.input_value = None 
        self.input_name = None
        self.tool_dir = None   
        self.tools = None

    def set_steps(self, tool_path):  
        self.load(steps_dir=tool_path) 
        self.tool_dir = tool_path  
        tools = [tool for tool in os.listdir(tool_path) if tool.endswith(".cwl")] 
        self.tools = [tool.split(".")[0] for tool in tools] 

    def set_input_value(self, input_value, input_name, input_type):   
        self.input_step = self.add_input(number=str(input_type)) # number is hard coded for now, but needs to be set to input_name
        self.input_value = input_value   
        self.input_name = input_name
    
    def generate_description(self):   
        tool_output = self.input_step 

        # for tool in self.tools:  
        #     tool_method = getattr(self, tool)   
        #     tool_output = tool_method(tool_output)  

        tool_output = self.sparc_data_tool(number=tool_output)  # sparc_data_tool is hard coded for now, but need to dynamically call 
                                                                # tool methods of workflow object based of tool name (str).
                                                                # an attempt is made above, but it doesn't work currently.

        self.add_outputs(final_answer=tool_output) 
        self.save(f'workflow.cwl', mode='abs')    
         
    def run(self, runner="cwltool"):  

         # subprocess.run(['cwltool', 
        #                 f'{self.tool_dir}/workflow.cwl', 
        #                 f'--{self.input_name}', str(self.input_value)]) 
     
        if(runner == "dockstore"):
            subprocess.run(['dockstore', 
                            'workflow', 
                            'launch',
                            '--local-entry'
                        f'{self.tool_dir}/workflow.cwl', 
                            '--json',
                        f'{self.tool_dir}/inp_job.json']) 
        else:
            subprocess.run(['cwltool', 
                            f'{self.tool_dir}/workflow.cwl', 
                            f'{self.tool_dir}/inp_job.json']) 

class Tool:  
        # create docstring below with methods, parameters and return values 
    """ 
    Tool class for generating CWL tools. 
    
    Parameters 
    ----------  
    tool_name : str, optional 
        Name of tool, e.g. sparc_data_tool. 
    
    tool_dir : str, optional 
        Path to directory where tool CWL file will be saved. 
    
    command : list, optional
        Command to run tool, e.g. ["python", "-m", "examples.sparc_workflow_example.tools.sparc_data_tool"]. 
    
    arguments : list, optional 
        Arguments to run tool, e.g. ["--number", "int"]. 
    
    input_type : str, optional 
        Type of input, e.g. int. 
    
    output_type : str, optional 
        Type of output, e.g. File. 
    
    output_path : str, optional 
        Path to output file, e.g. output.txt. 

    Attributes 

    Methods 
    ------- 
    set_tool_name(tool_name) 
        Sets the name of the tool. 
    
    set_tool_dir(tool_dir) 
        Sets the directory where the tool CWL file will be saved. 
    
    set_command(command) 
        Sets the command to run the tool. 
    
    set_arguments(arguments) 
        Sets the arguments to run the tool. 
    
    set_input_type(input_type) 
        Sets the type of input. 
    
    set_output_type(output_type) 
        Sets the type of output. 
    
    set_output_path(output_path) 
        Sets the path to the output file. 
    
    generate_description() 
        Generates the description of the tool, i.e. creates the CWL file. 
    ---------- 
    """
    def __init__(self, 
                 tool_name=None, 
                 tool_dir=None, 
                 command=None, 
                 arguments=None, 
                 input_type=None, 
                 output_type=None, 
                 output_path=None):  
        
        self.tool_name = tool_name 
        self.tool_dir = tool_dir 
        self.command = command 
        self.arguments = arguments 
        self.input_type = input_type 
        self.output_type = output_type 
        self.output_path = output_path 

    def set_tool_name(self, tool_name): 
        self.tool_name = tool_name  
    
    def set_tool_dir(self, tool_dir): 
        self.tool_dir = tool_dir

    def set_command(self, command):
        self.command = command

    def set_arguments(self, arguments):
        self.arguments = arguments

    def set_input_type(self, input_type):
        self.input_type = input_type

    def set_output_type(self, output_type):
        self.output_type = output_type

    def set_output_path(self, output_path):
        self.output_path = output_path 

    def generate_description(self):
        description = f"""#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: {self.command}

inputs:
    number:
        type: {self.input_type}
        inputBinding:
            position: 1 

outputs:
    output_file:
        type: {self.output_type}
        outputBinding:
            glob: {self.output_path}
                            """
        
        with open(f'{self.tool_dir}/{self.tool_name}.cwl', 'w') as f:
            f.write(description) 