#--------------------------------------------------------#
#                                                        #
#                                                        #
#                                                        #
#           UI designed to load LIDAR data in Maya       #
#                                                        #
#              Created on June, 29, 2015                 #
#              by: Jordan Alphonso                       #
#              email: jordanalphonso1@yahoo.com          #
#              Modified by: Roberto Aguirre              #
#              on: December 11, 2024                     #
#              email: raguirre@forensicrock.com          #
#--------------------------------------------------------#


#This was modified hastily and is likely unoptimized. I'm also not certain on how to launch this code other than the line at the end.

import maya.cmds as cmds
import os

class LIDARloader():

    #constructor
    def __init__( self ):

        #empty dictionary to store local variables
        self.widgets = {}

        #call the main window UI
        self.mainWindow()


    def mainWindow( self, *args ):

        #if window exists, then delete it
        if cmds.window( "mainWin", exists=True ):
            cmds.deleteUI( "mainWin" )

        #create main window and all components inside window
        self.widgets[ "mainWindow" ] = cmds.window( "mainWin", mnb=False, mxb=False, sizeable=False, title='LIDAR Loader' )
        cmds.window( self.widgets[ "mainWindow" ], edit=True, w=500, h=230 )

        self.widgets[ "mainLayout" ] = cmds.columnLayout()

        cmds.separator( h=10 )
        cmds.text( "Please select the LIDAR file you wish to load.", align='center', w=500 )
        cmds.separator( h=5 )

        cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 450), (2, 25)], columnOffset=[(1, 'left', 10), (2, 'left', 5)], w=500 )
        self.widgets[ "lidarPathField" ] = cmds.textField( editable=False, w=450 )
        self.widgets[ "browseButton" ] = cmds.button( label="+", w=25, c=self.browseButton )

        cmds.columnLayout()
        cmds. separator( h=10 )
        cmds.text( "Please enter the amount of points you would like to skip.\n"+
                    "(Hint: If this field is set to 1 then all LIDAR points will be loaded.)", align='center', w=500 )
        cmds.separator( h=5 )
        cmds.columnLayout( columnOffset=('left', 200) )
        self.widgets[ "skipField" ] = cmds.intField( editable=True, value=100, w=50 )

        cmds.columnLayout( parent=self.widgets[ "mainLayout" ], columnOffset=( 'left', 10 ) )
        cmds.separator( h=10 )
        self.widgets[ "executeButton" ] = cmds.button( label='Execute', w=470, c=self.executeButton )

        cmds.separator( h=5 )
        self.widgets[ "cancelButton" ] = cmds.button( label='Cancel', w=470, c=self.cancelButton )

        cmds.separator( h=20 )
        self.widgets[ "progressBar" ] = cmds.progressBar( w=470, progress=0 )


        #show window
        cmds.showWindow( self.widgets[ "mainWindow" ] )


    def browseButton( self, *args ):

        #pops up search window
        filterType = "*.pts"
        self.widgets[ "browseField" ] = cmds.fileDialog2( dialogStyle=2, caption='Load LIDAR', fileMode=1, fileFilter=filterType )

        cmds.textField( self.widgets[ "lidarPathField" ], edit=True, text=self.widgets[ "browseField" ][0] )


    def executeButton( self, *args ):

        #get value of lidar path
        lidarPath = cmds.textField( self.widgets[ "lidarPathField" ], query=True, text=True )

        #get skip number
        skipNumber = cmds.intField( self.widgets[ "skipField" ], query=True, value=True )

        i=1

        if lidarPath != "":

            lidarFile = open( lidarPath, 'r' )
            coordLines = lidarFile.readlines()

            lineCount = len( coordLines )
            cmds.progressBar( self.widgets[ "progressBar" ], edit=True, maxValue=(lineCount/skipNumber) )

            for line in coordLines[1::skipNumber]:

                #increment progress bar
                cmds.progressBar( self.widgets[ "progressBar" ], edit=True, progress=i )
                particleID = i-1
                i = i+1

                #split coords up into x y z
                coords = line.split( " " )

                coordX = coords[0]
                coordY = coords[1]
                coordZ = coords[2]
                
                red = float(coords[3])/255
                green = float(coords[4])/255
                blue = float(coords[5])/255

                ptt, ptc = cmds.particle( position=[coordX, coordY, coordZ])
                cmds.addAttr(ptc, longName = "rgbPP", dataType = "vectorArray")
                cmds.particle(ptc, e=True, at = "rgbPP", id=0, vv=(red, green, blue))


            #group the points for cleaniness
            selectedPart = cmds.select( 'particle*' )
            cmds.group( name='LIDAR_grp', world=True )

            #reset progress bar
            cmds.progressBar( self.widgets[ "progressBar" ], edit=True, progress=0 )



        else:
            cmds.warning( "No LIDAR file is selected." )


    def cancelButton( self, *args ):


        cmds.deleteUI( self.widgets[ "mainWindow" ] )

LIDARloader()
