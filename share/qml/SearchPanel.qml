/***************************************************************************************************
 *
 * Copyright (C) 2018 Fabrice Salvaire
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
    id: search_panel

    // anchors.fill: parent

    color: application_style.window_color

    ListModel {
        id: document_list_model
    }

    function fill_document_list() {
        for (var i = 0; i < 40; i++) {
	    var dict = {
		'path': 'path' + i,
		'title': 'Title ' + i
	    }
	    document_list_model.insert(i, dict)
	}
    }

    Component.onCompleted: {
        fill_document_list()
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Style.spacing.base
        spacing: Style.spacing.base_vertical

	RowLayout {
            Layout.fillWidth: true

	    ToolButton {
                iconSource: 'qrc:/icons/36x36/search-black.png'
		// onClicked:
	    }

	    TextField {
		id: query
		Layout.fillWidth: true
		placeholderText: qsTr("Enter query")
		onEditingFinished: console.info('Query', text)
	    }

	    ToolButton {
                iconSource: 'qrc:/icons/36x36/delete-black.png'
		onClicked: query.text = ''
	    }
	}

	ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            verticalScrollBarPolicy: Qt.ScrollBarAlwaysOn

            ListView {
                id: document_list
                width: parent.width
                spacing: Style.spacing.base_vertical

                model: document_list_model

                delegate: RowLayout {
                    width: parent.width

                    Button {
			// Layout.fillWidth: true
                        text: title
			style: ButtonStyle {
			    background: Rectangle {
				color: Qt.lighter(search_panel.color, control.pressed ? 0 : (control.hovered ? 5 : 0))
			    }
			}
                        onClicked: console.info('Clicked on document', title)
                    }
                }
            }
        }
    }
}