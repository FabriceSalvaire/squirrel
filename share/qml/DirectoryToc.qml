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
    id: directory_toc

    anchors.fill: parent

    // color: application_style.window_color

    ListModel {
        id: directory_list_model

	ListElement {
            name: 'Babel'
	}
	ListElement {
            name: 'BabelBuild'
	}
	ListElement {
            name: 'bin'
	}
	ListElement {
            name: 'build'
	}
	ListElement {
            name: 'devel-test'
	}
	ListElement {
            name: 'doc'
	}
	ListElement {
            name: 'ged-local'
	}
	ListElement {
            name: 'gh-pages'
	}
	ListElement {
            name: 'mupdf-examples'
	}
	ListElement {
            name: 'notes'
	}
	ListElement {
            name: 'old-vcs'
	}
	ListElement {
            name: 'pdf-pool'
	}
	ListElement {
            name: 'ressources'
	}
	ListElement {
            name: 'share'
	}
	ListElement {
            name: 'tools'
	}
	ListElement {
            name: 'trash'
	}
	ListElement {
            name: 'unit-test'
	}
	ListElement {
            name: 'user-scripts'
	}
	ListElement {
            name: 'workspace'
	}
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Style.spacing.base
        spacing: Style.spacing.base_vertical

	RowLayout {
            Layout.fillWidth: true

	    // ToolButton {
            Button {
                id: up_button
                iconSource: 'qrc:/icons/36x36/arrow-upward-black.png'
                text: 'upward'
                // onClicked:
	    }
	}

	Component {
            id: section_heading
            Rectangle {
		// width: container.width
		// This read-only property holds the collective position and size of the item's children.
		height: childrenRect.height

		Text {
                    text: section
                    font.bold: true
                    font.pixelSize: 20
		}
            }
	}

        ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            verticalScrollBarPolicy: Qt.ScrollBarAlwaysOn

            ListView {
                id: directory_list
                width: parent.width
                spacing: Style.spacing.small_vertical

                model: directory_list_model

                delegate: Button {
		    x: directory_list.x + 30
                    text: name
                    /*
                    style: ButtonStyle {
			background: Rectangle {
                            color: Qt.lighter(directory_toc.color, control.pressed ? 0 : (control.hovered ? 5 : 0))
			}
                    }
                    */
                    onClicked: console.info('Clicked on', name)
                }

		section.property: 'name'
		section.criteria: ViewSection.FirstCharacter
		section.delegate: section_heading
            }
        }
    }
}
