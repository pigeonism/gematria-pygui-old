#!/usr/bin/env python

# gui of gematria by wayne warren 2016 

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Gem(object):

    def __init__(self):
        # alpha ranges
        self.gem_six=[chr(i) for i in range(97,123)]
        self.gem_ord=self.gem_six[:]
        self.gem_heb=self.gem_ord[:]
        self.numer = {"ajs":1,"bkt":2,"clu":3,"dmv":4,"enw":5,"fox":6,"gpy":7,"hqz":8,"ir":9}

        self.build_lists(self) 
        

        # WINDOW
        #self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win = Gtk.Window()
        self.win.set_title("Gematria code test") 
        self.win.set_border_width(5)
        self.win.set_size_request(400,300)
        #self.win.set_position(Gtk.WIN_POS_CENTER)
        self.win.connect("destroy", self.die)

        # top panel
        self.word_text_label = Gtk.Label("Enter word(s) here:")
        self.word_text_in = Gtk.Entry()
        self.mid_box = Gtk.HBox()
        self.mid_box.pack_start(self.word_text_label, False,False,0)
        self.mid_box.pack_start(self.word_text_in, True,True,0)

        # mid 
        self.scrolled_window_res = Gtk.ScrolledWindow()
        #self.scrolled_window_res.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        self.text_view_results = Gtk.TextView()
        self.text_buffer_results = self.text_view_results.get_buffer()
        self.scrolled_window_res.add(self.text_view_results)
        self.second_lower_box = Gtk.HBox()
        self.second_lower_box.pack_start(self.scrolled_window_res,True,True,0)
        

        #last
        self.last_check_button = Gtk.Button("Check")
        self.last_check_button.connect("clicked", self.check_word) 
        
        self.last_clear_button = Gtk.Button("Clear")
        self.last_clear_button.connect("clicked", self.clear)

        self.last_box = Gtk.HBox()
        self.last_box.pack_start(self.last_check_button, False,False,0)
        self.last_box.pack_start(self.last_clear_button, False,False,0)

        #all
        self.big_box = Gtk.VBox(homogeneous=False)

        self.big_box.pack_start(self.mid_box,False,False,0)
        self.big_box.pack_start(self.second_lower_box,True,True,0)
        self.big_box.pack_start(self.last_box,False,False,0)


        self.win.add(self.big_box)
        self.win.show_all()

    ### Start-up methods
    def build_lists(self, widget):
        """ rebuild lists with values combined"""
        y=6
        for i in range(len(self.gem_six)):
            self.gem_six[i] += str(y)
            self.gem_ord[i] += str(i + 1)
            y+=6
        # traditional way, with eng alpha though
        heb=[1,2,3,4,5,6,7,8,9,600,10,20,30,40,50,60,70,80,90,100,200,700,900,300,400,500]
        for i in range(len(self.gem_heb)):
            self.gem_heb[i] += str(heb[i])

    ### Window methods
    def die(self, widget):
        """close"""
        Gtk.main_quit()

    def main(self):
        Gtk.main()

    def clear(self, widget):
        self.word_text_in.set_text("")
        #self.results_text_in.set_text("")
        self.text_buffer_results.set_text("")

    ## Helper methods
    def shorten(self, reduced):
        """ Reduce a number down to as few digits as possible"""
        if len(reduced) > 1:
                if len(reduced) ==2:
                        if reduced[0] == "0": return reduced[1]
                        if reduced[1] == "0": return reduced[0]
                else:
                        if "0" in reduced: reduced = reduced.replace("0", "")
                        if "9" in reduced: reduced = reduced.replace("9", "")

        test_total = 0
        test = list(reduced)
        if len(test) ==1:
                return test[0]
        

        else:
                for i in range(len(test)):
                        test_total += int(test[i])

        if len(str(test_total)) <= 1:
                return test_total
        else:
                reduced = self.shorten( str(test_total) )
                return reduced
        
        
    ### Widget methods
    def check_word(self, widget):
        """ Strip sentence to alphabetical characters and merge, then check values for each letter"""

        message = self.word_text_in.get_text()
        # remove non alpha's
        msg=""
        for letter in message:
            if letter == " ":
                pass
            if letter.isalpha() == False:
                pass
            else:
                msg += letter
        wstr = msg
        #print wstr

        six_total = 0
        ord_total = 0
        tra_total = 0
        
        for i in range(len(self.gem_six)):
                for j in range(len(wstr)):
                        if self.gem_six[i][0] == wstr[j]:
                                six_total += int(self.gem_six[i][1:])
                                
                        if self.gem_ord[i][0] == wstr[j]: # same len
                                ord_total += int(self.gem_ord[i][1:])

                        if self.gem_heb[i][0] == wstr[j]: # same len
                                tra_total += int(self.gem_heb[i][1:])

        # ord reduced
        ord_reduced = self.shorten( str(ord_total) )
        
        # numerology value
        num_total = 0
        for letter in wstr:
            for key in self.numer:
                if letter in key:
                    #print key, self.numer[key]
                    num_total += self.numer[key]
        numeral = self.shorten( str(num_total) )    

        results_txt =  "value using multiples of six\t: " + str(six_total) + "\n"
        results_txt += "ordinal values\t\t\t\t: " + str(ord_total) + "\n"
        results_txt += "ordinal reduced value\t\t: " + str(ord_reduced) + "\n"
        results_txt += "traditional value\t\t\t\t: " + str(tra_total) + "\n"
        results_txt += "numerological value\t\t\t: " + str(numeral) + "\n"
        # show results 
        self.text_buffer_results.set_text(results_txt)

if __name__ == "__main__":
    gem = Gem()
    gem.main()
