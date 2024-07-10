import datetime
import json


class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
              
        try:
            details = json.loads(request)
            if 'name' not in details or 'team_id' not in details:
                return json.dumps({'error': 'Missing required fields'})

            if len(details['name']) > 64:
                return json.dumps({'error': 'Board name must be 64 characters or less'})

            if 'description' in details and len(details['description']) > 128:
                return json.dumps({'error': 'Description must be 128 characters or less'})

            # Generate a unique ID for the board
            board_id = str(len(self.boards) + 1)
            details['id'] = board_id
            self.boards[board_id] = details

            return json.dumps({'id': board_id})
        except json.JSONDecodeError:
            return json.dumps({'error': 'Invalid JSON'})

# Example usage:
if __name__ == "_main_":
    board_manager = ProjectBoardBase()
    request_json = json.dumps({
        'name': 'New Project Board',
        'description': 'This is a sample board.',
        'team_id': 'team123'
    })
    response = board_manager.create_board(request_json)
    print(response)    
         
          
          
        

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        try:
          request_data = json.loads(request)
          board_id = request_data.get('id')
          
          if board_id != self.board_id:
            return json.dumps({"error":"Board id doesnot match"})
          
          if not self.are_all_tasks_complete():
            return json.dumps({"error":"Not all tasks are complete"})
          self.status = 'CLOSED'
          self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          return json.dumps({"status":"Board closed succesfully","end_time":self.end_time}) 
        
        except json.JSONDecodeError:
          return json.dumps({"error":"Invalid JSON"})
        except Exception as e:
          return json.dumps({"error":str(e)})
          
        
        

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        try:
          request_data = json.loads(request)
          title = request_data.get('title')
          description = request_data.get('description')  
          user_id = request_data.get('user_id')
          creation_time = request_data.get('creation_time')
          
          if self.status != 'OPEN':
            return json.dumps({"error":"Cannot add task to a closed board"})
          
          if  not self.is_title_unique(title):
            return json.dumps({"error":"Task title must be unique"})
          if len(title)> 64:
            return json.dumps({"error":"Title can be maximum of 64 characters"})
          if len(description)> 128:
            return json.dumps({"error":"Description can be maximum of 128 characters"})
           
          self.tasks.append(new_task) # type: ignore
          return json.dumps({"id":task_id}) # type: ignore
      
        except json.JSONDecodeError:
          return json.dumps({"error":"Invalid JSON"})
        except Exception as e:
          return json.dumps({"error":str(e)})
                            
                          
    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        try:
            request_data = json.loads(request)
            task_id = request_data.get('id')
            new_status = request_data.get('status')

            valid_statuses = {"OPEN", "IN_PROGRESS", "COMPLETE"}
            if new_status not in valid_statuses:
                return json.dumps({"error": "Invalid status"})

            task = self.find_task_by_id(task_id)
            if not task:
                return json.dumps({"error": "Task ID not found"})

            task['status'] = new_status
            return json.dumps({"status": "Task status updated successfully"})

        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        try:
            request_data = json.loads(request)
            team_id = request_data.get('id')

            if team_id != self.team_id:
                return json.dumps({"error": "Team ID does not match"})

            board_list = []
            for board in self.boards:
                board_list.append({"id": board.board_id, "name": board.name})

            return json.dumps(board_list)

        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        try:
            request_data = json.loads(request)
            board_id = request_data.get('id')

            if board_id != self.board_id:
                return json.dumps({"error": "Board ID does not match"})

            filename = f"board_export_{board_id}{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(f"Board Name: {self.name}\n")
                f.write("Tasks:\n")
                for idx, task in enumerate(self.tasks, start=1):
                    f.write(f"Task {idx}:\n")
                    f.write(f"  Title: {task.get('title', '')}\n")
                    f.write(f"  Description: {task.get('description', '')}\n")
                    f.write(f"  Status: {task.get('status', '')}\n")
                    f.write(f"  Assigned User ID: {task.get('user_id', '')}\n")
                    f.write(f"  Creation Time: {task.get('creation_time', '')}\n\n")

            return json.dumps({"out_file": filename})

        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON"})
        except Exception as e:
            return json.dumps({"error": str(e)})
