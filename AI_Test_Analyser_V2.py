import google.generativeai as genai

genai.configure(api_key="AIzaSyA7BFAU6rBnDTjUoWKkysfTvaNAe0Yj7cU")

def analyze_test_answers(questions, student_answers):
    """
    Analyzes student answers using a Generative AI model to gauge understanding.

    Args:
        questions (list): A list of the test questions.
        student_answers (list): A list of the student's answers, corresponding to the questions.

    Returns:
        tuple: A tuple containing:
            - list: A list of estimated percentages of understanding for each question.
            - str: The AI's analysis of the student's overall performance.
    """

 
    if not (len(questions) == len(student_answers)):
        print("Error: The number of questions and student answers must be the same.")
        return [0.0] * len(questions), "Error: Inconsistent input lengths."

    prompt = "You are a helpful assistant, tasked with assessing a student's understanding of a topic based on their answers to test questions.  Here are the questions and the student's answers:\n\n"
    for i, question in enumerate(questions):
        prompt += f"Question {i+1}: {question}\n"
        prompt += f"Student Answer {i+1}: {student_answers[i]}\n\n"

    prompt += "Analyze the student's answers.  Provide an estimate of the student's understanding for each question as a percentage on a new line. Base the percentage on the clarity, accuracy, and completeness of their answers. After the percentages, provide a summary of the student's overall performance, highlighting areas where they demonstrated good understanding and areas where they need to improve.  Keep the analysis concise and constructive.\n\n"
    prompt += "Example Output:\n"
    prompt += "1. 100%\n"
    prompt += "2. 70%\n"
    prompt += "3. 90%\n"
    prompt += "4. 60%\n"
    prompt += "5. 80%\n"
    prompt += "Analysis: The student demonstrates a good understanding of the basic concepts. They answered questions 1, 3, and 5 clearly and accurately. However, their answers to questions 2 and 4 suggest some confusion with more advanced topics. They should review those topics for a better grasp of the material.\n\n"
    prompt += "Provide your analysis in the same format but with more detail."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        ai_analysis = response.text

        percentages = []
        lines = ai_analysis.splitlines()
        for line in lines:
            if line.startswith(tuple(f"{i+1}. " for i in range(len(questions)))):
                try:
                    percentage = float(line.split()[1].replace("%", ""))
                    percentages.append(percentage)
                except ValueError:
                    percentages.append(0.0)

        summary_start = -1
        for i, line in enumerate(lines):
            if line.startswith("Analysis:"):
                summary_start = i
                break
        summary = "\n".join(lines[summary_start:]) if summary_start != -1 else "No summary found."


        return percentages, summary

    except Exception as e:
        print(f"An error occurred: {e}")
        return [0.0] * len(questions), f"Error: {e}"

if __name__ == "__main__":
    # Sample test data.
    questions = [
        "What is a binary search tree?",
        "Explain the difference between a stack and a queue.",
        "What is the time complexity of accessing an element in an array?",
        "Describe how a hash table works.",
        "What is the purpose of a linked list?",
        "Explain the concept of recursion.",
        "What is a graph data structure?",
        "Describe the difference between depth-first search (DFS) and breadth-first search (BFS).",
        "What is the time complexity of sorting an array using merge sort?",
        "Explain the difference between a balanced and unbalanced binary search tree.",
    ]
    student_answers = [
        "A binary search tree is a tree, where nodes are organized in a specific order, but that order isn't fully defined.",  # Partially correct
        "A stack is like a pile of plates where you can only take the top one off, and a queue is like a line at a store where the first person in line is served first.",  # Partially correct
        "O(1).",  # Correct
        "It uses a function to store data, but doesn't really explain how the function works or handles collisions.",  # Partially correct
        "Linked lists are used to store data in a sequence, but the elements aren't in consecutive memory locations.",  # Partially correct
        "Recursion is when a function calls itself to solve a problem by breaking it down into smaller, self-similar subproblems.",  # Correct
        "A graph is made of nodes and lines, showing relationships between data points, but doesn't specify directed or undirected.",  # Partially correct
        "DFS goes deep into a branch before exploring other branches, and BFS explores all neighbors at the current level before going deeper.",  # Partially correct
        "It's O(n log n).",  # Correct
        "Balanced trees are better in terms of performance, but doesn't explain why."  # Partially correct
    ]


    percentages, analysis = analyze_test_answers(questions, student_answers)

    for i, percentage in enumerate(percentages):
        print(f"{i+1}. {percentage:.2f}%")
    print("AI Analysis:\n", analysis)

