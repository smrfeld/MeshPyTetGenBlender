def export_to_xml(fname, vert_list, tet_list):

    # Open
    f = open(fname, "w")

    # Write
    f.write('<dolfin xmlns:dolfin="http://www.fenics.org/dolfin/">\n')
    f.write('   <mesh celltype="tetrahedron" dim="3">\n')
    f.write('       <vertices size=" %i">\n' % len(vert_list))
    for i in range(0,len(vert_list)):
        f.write('           <vertex index=" %i" x=" %.5f " y=" %.5f " z=" %.5f "/>\n' % (i,vert_list[i][0],vert_list[i][1],vert_list[i][2]))
    f.write('       </vertices>\n')
    f.write('       <cells size=" %i">\n' % len(tet_list))
    for i in range(0,len(tet_list)):
        f.write('           <triangle index=" %i" v0=" %i" v1=" %i" v2=" %i" v3=" %i"/>\n' % (i,tet_list[i][0],tet_list[i][1],tet_list[i][2],tet_list[i][3]))
    f.write('       </cells>\n')
    f.write('   </mesh>\n')
    f.write('</dolfin>\n')

    # Close
    f.close()
