/***************************************************************************************************
 *
 * Copyright (C) 2017 Fabrice Salvaire
 * Contact: http://www.fabrice-salvaire.fr
 *
 * This file is part of the Babel software.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0

import Constants 1.0

Rectangle {
    id: path_navigator

    anchors.fill: parent

    color: application_style.window_color

    ListModel {
        id: path_model
    }

    ListModel {
        id: directory_model
    }

    function fill_model() {
        for (var i = 0; i < 10; i++)
            path_model.insert(i, {'name': 'dir' + i})
        for (var i = 0; i < 10; i++)
            directory_model.insert(i, {'name': 'dir' + i})
    }

    Component.onCompleted: {
        console.info('PathNavigator')
        fill_model()
    }

     ListView {
        anchors.fill: parent
        anchors.margins: Style.spacing.base
        orientation: ListView.Horizontal
        spacing: 3 // Style.spacing.base_horizontal

        model: path_model

        delegate: Row {
            Button {
                text: name
                style: ButtonStyle {
                    background: Rectangle {
                        color: Qt.lighter(path_navigator.color, control.pressed ? 0 : (control.hovered ? 5 : 0))
                    }
                }
                onClicked: {
                    console.info('Clicked on directory', model.index)
                }
            }
	    Menu {
                id: menu
                iconSource: 'qrc:/icons/36x36/chevron-left-black.png'

                Instantiator {
                    model: directory_model
                    onObjectAdded: menu.insertItem(index, object)
                    onObjectRemoved: menu.removeItem(object)
                    delegate: MenuItem {
                        text: name
                        onTriggered: console.info('clicked on directory', name)
                    }
                }
	    }
            ToolButton {
                iconSource: 'qrc:/icons/36x36/chevron-right-black.png'
                onClicked: menu.open()
            }
        }
    }
}
