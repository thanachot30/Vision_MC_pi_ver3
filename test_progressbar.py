from tkinter import *
from tkinter import ttk


class Cinema():
    def __init__(self, root):
        self.root = root
        title = Label(self.root, text="Bravo Cinema", font=(
            "Helvetica", 40, "bold"), foreground="orange", background="#46464a").pack()

        # main navigation buttons
        self.movies = Button(self.root, text="View Movies", font=("Helvetica", 15), fg="orange", bg="#46464a", activeforeground="orange", activebackground="#2c2c2e", cursor="hand2",
                             command=self.view_movies_UI)
        self.movies.place(x=30, y=110)

        self.add_movie = Button(self.root, text="Add Movie", font=("Helvetica", 15), fg="orange", bg="#46464a", activeforeground="orange", activebackground="#2c2c2e", cursor="hand2",
                                command=self.add_movie_UI)
        self.add_movie.place(x=185, y=110)

        self.bookings = Button(self.root, text="View Bookings", font=("Helvetica", 15), fg="orange", bg="#46464a", activeforeground="orange", activebackground="#2c2c2e", cursor="hand2",
                               command=self.view_bookings_UI)
        self.bookings.place(x=320, y=110)

        self.frame1 = Frame(self.root, background="#46464a")
        self.frame1.place(x=0, y=160)

    # view movies
    def view_movies_UI(self):
        # label

        try:

            for widget in self.frame1.winfo_children():
                widget.destroy()

        except:
            pass

        lbl_all_movies = Label(self.frame1, text="All movies", font=(
            "Helvetica", 13), bg="#46464a", fg="orange")
        lbl_all_movies.pack()
        movies_frame = Frame(self.frame1, bg="white")
        movies_frame.pack()

        # tree view table
        movie_tree = ttk.Treeview(
            movies_frame, column=("#1", "#2"), show='headings')

        #columns and headings
        movie_tree.column("#1", anchor=CENTER, width=60)
        movie_tree.column("#2", anchor=CENTER, width=110)
        movie_tree.heading("#1", text="ID")
        movie_tree.heading("#2", text="Name")
        movie_tree.pack()

    # add movie
    def add_movie_UI(self):

        try:

            for widget in self.frame1.winfo_children():
                widget.destroy()

        except:
            pass

        # entry boxes
        lbl_movie_name = Label(self.frame1, text="Movie Name:", font=(
            "Ariel", 11), bg="#46464a", fg="white")
        lbl_movie_name.pack()
        txt_movie_name = Entry(self.frame1, font=(
            "Ariel", 10), width=40, bg="#46464a", fg="white")
        txt_movie_name.pack()

        lbl_run_time = Label(self.frame1, text="Movie Length (minutes):", font=(
            "Ariel", 11), bg="#46464a", fg="white")
        lbl_run_time.pack()
        txt_run_time = Entry(self.frame1, font=(
            "Ariel", 10), width=40, bg="#46464a", fg="white")
        txt_run_time.pack()

        lbl_genre = Label(self.frame1, text="Movie Genre/Genres:",
                          font=("Ariel", 11), bg="#46464a", fg="white")
        lbl_genre.pack()
        txt_genre = Entry(self.frame1, font=("Ariel", 10),
                          width=40, bg="#46464a", fg="white")
        txt_genre.pack()

    # view bookings
    def view_bookings_UI(self):

        try:

            for widget in self.frame1.winfo_children():
                widget.destroy()

        except:
            pass

        # label
        lbl_all_bookings = Label(self.frame1, text="All Bookings", font=(
            "Helvetica", 13), bg="#46464a", fg="orange")
        lbl_all_bookings.pack()

        bookings_frame = Frame(self.frame1, bg="white")
        bookings_frame.pack()

        # tree view table
        booking_tree = ttk.Treeview(
            bookings_frame, column=("#1"), show='headings')

        #columns and headings
        booking_tree.column("#1", anchor=CENTER, width=60)
        booking_tree.heading("#1", text="ID")
        booking_tree.pack()


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x700")
    root.title("Bravo Cinema")
    root.configure(background="#46464a")
    bravo = Cinema(root)
    root.mainloop()
