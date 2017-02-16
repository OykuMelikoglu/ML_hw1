import numpy as np
import matplotlib.pyplot as plt


class Solver:
    cost_function = ""  # MSE or MAE
    test_file_name = ""  # name of the test file
    training_file_name = ""  # name of the training file
    target_name = " "  # G1, G2, G3, Lat or Lon
    learning_rate = 0.0  # value of alpha
    repetition = 0  # number of iterations
    batch_size = 0  # batch size for mini batch gradient
    delimiter = ","  # the files are split via commas
    training_x = []  # x values gathered from the training data
    test_x = []  # x values gathered from the test data
    training_y = []  # y values gathered from the training data
    test_y = []  # y values gathered from the test data
    beta = []  # beta values
    momentum = 0.0  # momentum constant
    update_vector = []  # vector to hold velocity constants
    momentum_on = False  # 0 - Off, 1 - On
    iteration_cost_history = []  # iteration cost tuple history used for plotting graph
    task_num = ""  # task to operate

    def initialize(self):
        """
        Initializing the constants and the user desired selections
        """
        if self.task_num == "1_MSE":  # Task1 MSE
            self.cost_function = "MSE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G1"
        elif self.task_num == "1_MAE":  # Task1 MAE
            self.cost_function = "MAE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G1"
        elif self.task_num == "2_MSE":  # Task2 MSE
            self.cost_function = "MSE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G2"
        elif self.task_num == "2_MAE":  # Task2 MAE
            self.cost_function = "MAE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G2"
        elif self.task_num == "3_MSE":  # Task3 MSE
            self.cost_function = "MSE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G3"
        elif self.task_num == "3_MAE":  # Task3 MAE
            self.cost_function = "MAE"
            self.training_file_name = "studentTraining.txt"
            self.test_file_name = "studentTest.txt"
            self.target_name = "G3"
        elif self.task_num == "4_MSE":  # Task4 MSE
            self.cost_function = "MSE"
            self.training_file_name = "geoTraining.txt"
            self.test_file_name = "geoTest.txt"
            self.target_name = "Lat"
        elif self.task_num == "4_MAE":  # Task4 MAE
            self.cost_function = "MAE"
            self.training_file_name = "geoTraining.txt"
            self.test_file_name = "geoTest.txt"
            self.target_name = "Lat"
        elif self.task_num == "5_MSE":  # Task5 MSE
            self.cost_function = "MSE"
            self.training_file_name = "geoTraining.txt"
            self.test_file_name = "geoTest.txt"
            self.target_name = "Lon"
        elif self.task_num == "5_MAE":  # Task5 MAE
            self.cost_function = "MAE"
            self.training_file_name = "geoTraining.txt"
            self.test_file_name = "geoTest.txt"
            self.target_name = "Lon"

        self.read_file()

    def read_file(self):
        """
        Putting the data into lists
        """
        if self.test_file_name == "studentTest.txt":
            # initializing lists from test file
            with open(self.test_file_name, "r") as test_file:
                for line in test_file:
                    data = line.replace('\n', '').split(',')
                    self.test_x.append(list(map(float, data[:43])))
                    self.test_y.append(list(map(float, data[-3:])))
            # initializing lists from training file
            with open(self.training_file_name, "r") as training_file:
                for line in training_file:
                    data = line.replace('\n', '').split(',')
                    self.training_x.append(list(map(float, data[:43])))
                    self.training_y.append(list(map(float, data[-3:])))
        else:
            # initializing lists from test file
            with open(self.test_file_name, "r") as test_file:
                for line in test_file:
                    data = line.replace('\n', '').split(',')
                    self.test_x.append(list(map(float, data[:116])))
                    self.test_y.append(list(map(float, data[-2:])))
            # initializing lists from training file
            with open(self.training_file_name, "r") as training_file:
                for line in training_file:
                    data = line.replace('\n', '').split(',')
                    self.training_x.append(list(map(float, data[:116])))
                    self.training_y.append(list(map(float, data[-2:])))

        # Adding 1 in front of the sets to have 1xB0
        for i in range(0, len(self.training_x)):
            self.training_x[i].insert(0, 1.0)
        for i in range(0, len(self.test_x)):
            self.test_x[i].insert(0, 1.0)

        self.compute()
        self.draw()

    def compute(self):
        """
        Trains and gets the values of the error from the cost function
        """
        self.beta = np.ones(len(self.training_x[0]))  # initializing beta values to 1s
        self.update_vector = np.ones(len(self.training_x[0]))  # initializing update vector values to 0s
        # initialize the target value to be chosen from the target datas
        if self.target_name == "G1" or self.target_name == "Lat":
            y_index = 0
        elif self.target_name == "G2" or self.target_name == "Lon":
            y_index = 1
        else:
            y_index = 2
        # calculate betas and get the error result and iterate repetition times
        for i in range(0, self.repetition):
            self.calculate_betas(y_index)
            if self.cost_function == "MSE":
                # adding to list to draw the graph
                self.iteration_cost_history.append((i, self.calculate_mse(y_index)))
            else:
                # adding to list to draw the graph
                self.iteration_cost_history.append((i, self.calculate_mae(y_index)))
            print("Iteration:", i)

    def draw(self):
        """
        Draws the graph with the values gathered from iteration_cost_history
        """
        x_val = []
        y_val = []
        for i in range(0, len(self.iteration_cost_history)):
            x_val.append(self.iteration_cost_history[i][0])  # number of iterations
            y_val.append(self.iteration_cost_history[i][1])  # cost error value
        plt.ylabel(self.cost_function)  # initializing label for the y axis
        plt.xlabel("Number of Times Iterated")  # initializing label for the x axis
        title = "Graph for Task: " + self.task_num + " Momentum: " + str(self.momentum_on)  # initializing graph name
        plt.title(title)
        plt.plot(x_val, y_val, 'r')
        plt.show()

    def calculate_target(self, index):
        """
        Calculates dot product value for test dataset
        :param index: which instance is used to calculate dot product
        :return: float dot product result (b0x0 + b1x1 + b2x2 + ...)
        """
        return float(np.dot(self.test_x[index], self.beta))

    def calculate_mse(self, y_index):
        """
        Calculates Mean Squared Error
        :param y_index: chosen target index (G1|Lon or G2|Lat or G3)
        :return: mse value as a result
        """
        result = 0.0
        for index in range(0, len(self.test_x)):
            # gets the sum of squared (hypothesis-target) for each instance
            result += (self.calculate_target(index) - self.test_y[index][y_index]) ** 2
        # gets the average of the sum
        return result / len(self.test_x)

    def calculate_mae(self, y_index):
        """
        Calculates Mean Absolute Error
        :param y_index: chosen target index (G1|Lon or G2|Lat or G3)
        :return: mae value as a result
        """
        result = 0.0
        for index in range(0, len(self.test_x)):
            # gets the sum of squared (hypothesis-target) for each instance
            result += np.fabs(self.calculate_target(index) - self.test_y[index][y_index])
        # gets the average of the sum
        return result / len(self.test_x)

    def calculate_betas(self, y_index):
        """
        Determining the beta values
        :param y_index: chosen target index (G1|Lon or G2|Lat or G3)
        """
        temp = 0.0
        # for each beta, iterate through all instances but separate them between different batches by given batch size
        for betas in range(0, len(self.beta)):
            for inst in range(0, len(self.training_x)):
                if self.cost_function == "MSE":
                    temp += ((np.dot(self.training_x[inst], self.beta) - self.training_y[inst][y_index]) *
                             self.training_x[inst][betas]) / self.batch_size
                else:  # if mae is wanted to be calculated
                    temp += (-self.training_x[inst][betas]) / (
                        np.fabs(np.dot(self.training_x[inst], self.beta)) - self.training_y[inst][
                            y_index]) * self.batch_size
                # if the end of batch is reached or instances are finished (number of instances in a batch may slightly
                # differ if the dividend is not a power of the divisor ) , calculate beta
                if (inst % self.batch_size == self.batch_size - 1) or inst == len(self.training_x) - 1:
                    if self.momentum_on:
                        self.update_vector[betas] = (self.momentum * self.update_vector[betas]) - (
                            self.learning_rate * temp)
                        self.beta[betas] += self.update_vector[betas]
                    else:  # if momentum is not selected
                        self.beta[betas] -= temp * self.learning_rate
                    temp = 0.0  # reset temp value
            temp = 0.0  # reset temp value


def main():
    solver = Solver()

    solver.learning_rate = 0.001
    solver.repetition = 100
    solver.batch_size = 8
    solver.momentum = 0.6
    solver.momentum_on = False  # uncomment if momentum is off
    # solver.momentum_on = True  # uncomment if momentum is on

    solver.task_num = "1_MSE"  # uncomment to predict G1 with MSE
    # solver.task_num = "1_MAE"  # uncomment to predict G1 with MAE
    # solver.task_num = "2_MSE"  # uncomment to predict G2 with MSE
    # solver.task_num = "2_MAE"  # uncomment to predict G2 with MAE
    # solver.task_num = "3_MSE"  # uncomment to predict G3 with MSE
    # solver.task_num = "3_MAE"  # uncomment to predict G3 with MAE
    # solver.task_num = "4_MSE"  # uncomment to predict Latitude with MSE
    # solver.task_num = "4_MAE"  # uncomment to predict Latitude with MAE
    # solver.task_num = "5_MSE"  # uncomment to predict Longitude with MSE
    # solver.task_num = "5_MAE"  # uncomment to predict Longitude with MAE

    solver.initialize()


if __name__ == '__main__':
    main()
