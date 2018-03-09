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

import Constants 1.0

Rectangle {
    id: destination_list

    anchors.fill: parent

    color: application_style.window_color

    ListModel {
        id: destination_list_model
    }

    function fill_destination_list() {
        for (var i = 0; i < 50; i++)
            destination_list_model.insert(i, {'name': 'dir' + i})
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Style.spacing.base
        spacing: Style.spacing.base_vertical

	RowLayout {
            Layout.fillWidth: true

	    ToolButton {
                id: add_destination_button
                iconSource: 'qrc:/icons/36x36/playlist-add-black.png'
                // Fixme: don't work ???
                // iconSource: 'image://icon_provider/playlist-add-black@36'
                onClicked: fill_destination_list()
	    }
	    ToolButton {
                id: clear_button
                iconSource: 'qrc:/icons/36x36/delete-black.png'
                onClicked: destination_list_model.clear()
	    }
	}

        ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            verticalScrollBarPolicy: Qt.ScrollBarAlwaysOn

            ListView {
                id: directory_list
                width: parent.width
                spacing: Style.spacing.base_vertical

                model: destination_list_model

                delegate: RowLayout {
                    width: parent.width

                    Button {
                        Layout.fillWidth: true
                        text: name
                        onClicked: console.info('Clicked on destination', model.index)
                    }
	            ToolButton {
                        iconSource: 'qrc:/icons/36x36/delete-black.png'

                        onClicked: destination_list_model.remove(model.index)
	            }
                }
            }
        }
    }

    Component.onCompleted: {
        // fill_destination_list()
    }
}
